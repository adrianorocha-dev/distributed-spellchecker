import socket, json

s = socket.socket()

s.connect(('10.180.15.183', 12345))

s.send(json.dumps('asdkjs asdkjas asdj,asmda asdjk, sa').encode(encoding='utf-8'))

result = s.recv(1024).decode(encoding='utf-8')

wrong_indices = json.loads(result)

print(wrong_indices)