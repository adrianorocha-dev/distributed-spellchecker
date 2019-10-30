import socket

s = socket.socket()

s.connect(('localhost', 12345))

print(s.recv(1024).decode())

s.send("testando".encode())