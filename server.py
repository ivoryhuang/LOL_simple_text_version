import socket
import _thread

from champs import Brand, Ziggs
from games import ARAM, Item_Shop
from items import *

class Server():
    def __init__(self):
        self.socket = None
        self.host = socket.gethostname() 
        self.port = 9487

    def create_socket(self):
        self.socket = socket.socket()
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.host, self.port))
        self.socket.listen(5)
        print('---------ARAM starts---------')

    def listen(self):
        player_idx = -1
        while True:
           client, addr = self.socket.accept()
           player_idx += 1
           print('Got connection from', addr, 'player_idx', player_idx)
           player = Player(player_idx=player_idx, socket=client, server=server)
           player.get_champ()
           _thread.start_new_thread(player.connect, ())

        self.socket.close()

    def send_msg(self, msg, c_socket):
        c_socket.send(msg.encode())

    def send_initial_msg(self, player):
        self.send_msg('You are %s' % (player.champ.name), player.socket)
        self.send_msg('\nYou want to: (1)Move (2)See the location of champions (3)Buy items (4)Sell items (5)See own items and gold (6)Attack', player.socket)



class Player():
    def __init__(self, player_idx=None, socket=None, server=None):
        self.player_idx = player_idx
        self.socket = socket
        self.server = server
        self.champ = None

    def get_champ(self):
        champ_idx = aram.random_assign_champ()
        self.champ = aram.champs[champ_idx]

    def connect(self):
        self.server.send_initial_msg(self)
        while True:
            choice = self.socket.recv(1024).decode()
            print('choice', choice)

            #move
            if choice == '1':
                self.server.send_msg('Input coordinate(from 0,0 to 10000,10000), e.g. 20,25 :', self.socket)
                coord = self.socket.recv(1024).decode().split(',')
                x = int(coord[0])
                y = int(coord[1])
                result = self.champ.move((x, y))
                self.server.send_msg(result, self.socket)

            #print everyone's location
            elif choice == '2':
                for self.player_idx, self.champ in aram.champs.items():
                    self.server.send_msg(self.champ.display_coord()+'\n', self.socket)

            #buy itmes
            elif choice == '3':
                self.server.send_msg(item_shop.display_items_to_sell(), self.socket)
                item_code = int(self.socket.recv(1024).decode())
                self.server.send_msg(self.champ.buy_item(item_code), self.socket)

            #sell items
            elif choice == '4':
                self.server.send_msg(item_shop.display_items_to_recycle(self.champ), self.socket)
                item_idx = int(self.socket.recv(1024).decode())
                self.server.send_msg(self.champ.sell_item(item_idx-1), self.socket)

            #see items and gold
            elif choice == '5':
                self.server.send_msg("$%d\n%s" % (self.champ.gold, str(self.champ.display_items())), self.socket)

            self.server.send_msg('\nYou want to: (1)Move (2)See the location of champions (3)Buy items (4)Sell items (5)See own items and gold (6)Attack', self.socket)

        self.socket.close()

aram = ARAM()
item_shop = Item_Shop()
Brand = Brand(aram_center=aram, team_idx=0, member_idx=0, item_shop=item_shop)
Ziggs = Ziggs(aram_center=aram, team_idx=1, member_idx=1, item_shop=item_shop)
aram.compose_team([Brand, Ziggs])

server = Server()
server.create_socket()
server.listen()