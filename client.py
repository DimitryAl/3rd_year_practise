import socket

client_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_sock.connect(('127.0.0.1', 53210))
#client_sock.sendall(b'Hello, world')
#data = client_sock.recv(1024)
#client_sock.close()
#print('Received', repr(data))
while True:
    message = input()
    client_sock.sendall(message.encode('utf-8'))
    data = client_sock.recv(1024)
    print('Received', repr(data))
