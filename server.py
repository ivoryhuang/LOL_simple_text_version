import socket
import _thread

from champs import Brand, Ziggs
from games import ARAM, Item_Shop
from items import *

aram = ARAM()
item_shop = Item_Shop()
Brand = Brand(aram_center=aram, team_idx=0, member_idx=0, item_shop=item_shop)
Ziggs = Ziggs(aram_center=aram, team_idx=1, member_idx=1, item_shop=item_shop)
aram.compose_team([Brand, Ziggs])


def send_msg(msg, c):
    c.send(msg.encode())

def handle_client(c, player_idx):
    
    champ_idx = aram.random_assign_champ()
    champ = aram.champs[champ_idx]

    send_msg('You are %s' % (champ.name), c)
    send_msg('\nYou want to: (1)Move (2)See the location of champions (3)Buy items (4)Sell items (5)See own items and gold (6)Attack', c)
    
    while True:
        choice = c.recv(1024).decode()
        print('choice', choice)

        #move
        if choice == '1':
            send_msg('Input coordinate(from 0,0 to 10000,10000), e.g. 20,25 :', c)
            coord = c.recv(1024).decode().split(',')
            x = int(coord[0])
            y = int(coord[1])
            result = champ.move((x, y))
            send_msg(result, c)

        #print everyone's location
        elif choice == '2':
            for player_idx, champ in aram.champs.items():
                send_msg(champ.display_coord()+'\n', c)

        #buy itmes
        elif choice == '3':
            send_msg(item_shop.display_items_to_sell(), c)
            item_code = int(c.recv(1024).decode())
            send_msg(champ.buy_item(item_code), c)

        #sell items
        elif choice == '4':
            send_msg(item_shop.display_items_to_recycle(champ), c)
            item_idx = int(c.recv(1024).decode())
            send_msg(champ.sell_item(item_idx-1), c)

        #see items and gold
        elif choice == '5':
            send_msg("$%d\n%s" % (champ.gold, str(champ.display_items())), c)

        send_msg('\nYou want to: (1)Move (2)See the location of champions (3)Buy items (4)Sell items (5)See own items and gold (6)Attack', c)

    c.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = socket.gethostname() 
PORT = 9487

print('---------ARAM starts---------')

s.bind((HOST, PORT))
s.listen(5)
player_idx = -1
while True:
   client, addr = s.accept()
   player_idx += 1
   send_msg(str(player_idx), client)
   print('Got connection from', addr, 'player_idx', player_idx)
   _thread.start_new_thread(handle_client, (client, player_idx))

s.close()