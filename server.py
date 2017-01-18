import socket
import _thread

from champs import Brand, Ziggs
from games import ARAM
from items import *

aram = ARAM()
Brand = Brand(aram_center=aram, team_idx=0, member_idx=0)
Ziggs = Ziggs(aram_center=aram, team_idx=1, member_idx=1)
aram.compose_team([Brand, Ziggs])

def send_msg(msg, c):
    c.send(msg.encode())

def handle_client(c, player_idx):
    
    champ_idx = aram.random_assign_champ()
    champ = aram.champs[champ_idx]

    send_msg('You are %s' % (champ.name), c)
    send_msg('\nYou want to: (1)Move (2)See the location of other champions (3)Buy items (4)Attack', c)
    
    while True:
        choice = c.recv(1024).decode()
        print('choice', choice)

        #move
        if choice == '1':
            send_msg('Input coordinate(from 0,0 to 10000,10000), e.g. 20,25 :', c)
            coord = c.recv(1024).decode().split(',')
            x = int(coord[0])
            y = int(coord[1])
            print('player_idx', player_idx)
            result = aram.champs[player_idx].move((x, y))
            send_msg(result, c)

        #print everyone's location
        elif choice == '2':
            for player_idx, champ in aram.champs.items():
                send_msg(champ.display_coord()+'\n', c)

        #buy itmes
        elif choice == '3':
            pass
        #choose attack
        elif choice == '4':
            msg = 'Attack '

        send_msg('\nYou want to: (1)Move (2)See the location of other champions (3)Buy items (4)Attack', c)

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