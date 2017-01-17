import socket
import _thread

from champs import Brand, Ziggs
from games import ARAM
from items import *

aram = ARAM()
Brand = Brand(aram_center=aram, team_idx=0, member_idx=0)
Ziggs = Ziggs(aram_center=aram, team_idx=1, member_idx=1)
aram.compose_team([Brand, Ziggs])

def handle_client(c_socket, addr):
   
    msg = 'You are %s\n' % (aram.champs[aram.random_assign_champ()].name)
    c_socket.send(msg.encode())
    msg = 'You want to: (1)Move (2)Buy items (3)See the location of other champions (4)Attack'
    c_socket.send(msg.encode())
    
    while True:
        choice = c_socket.recv(1024).decode()
        print(choice)

        #move
        if choice == '1':
            print('move to')
            msg = 'Move to'

        #buy itmes
        elif choice == '2':
            msg = 'Buy '

        #print everyone's location
        elif choice == '3':
            msg = 'Champs '

        #choose attack
        elif choice == '4':
            msg = 'Attack '

        c_socket.send(msg.encode())

    c_socket.close()

s = socket.socket()
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
HOST = socket.gethostname() 
PORT = 9487

print('---------ARAM starts---------')

s.bind((HOST, PORT))
s.listen(5)

while True:
   c, addr = s.accept()
   print('Got connection from', addr)
   _thread.start_new_thread(handle_client, (c, addr))

s.close()