import socket, sys

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except(socket.error, msg):
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    sys.exit(1)

HOST = socket.gethostname()
PORT = 9487

try:
    s.connect((HOST, PORT))
except(socket.error, msg):
    sys.stderr.write("[ERROR] %s\n" % msg[1])
    exit(1)

print('---------ARAM starts---------')
print(s.recv(1024).decode())
print(s.recv(1024).decode())

while True:
    msg = input()
    if not msg:
        continue
    s.send(msg.encode())
    print(s.recv(1024).decode())

s.close()