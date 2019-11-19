import socket, json
from spellchecker import SpellChecker
import time

config = json.loads(open('config.json').read())
print('loaded config: ', config)

# Function to connect to the head and offer processing
def connect_to_head():
    ping_socket = socket.socket()
    ping_socket.connect((config['head_ip'], config['ping_port']))

    ping_socket.send('connect'.encode(encoding='utf-8'))

    ping_socket.close()

def calculate_bill(n_words):
    return n_words * config['price_per_word']

connect_to_head()

s = socket.socket()

s.bind(('', 12345))

s.listen(5)

spellchecker = SpellChecker()

while(True):
    print('Waiting for connection')
    c, addr = s.accept()

    print('{} connected.'.format(addr))

    msg = ''

    while True:
        b = c.recv(4096)
        msg += b.decode(encoding='utf-8')
        if len(b) < 4096:
            break


    print("received: {}".format(msg))

    if msg == 'ping':
        c.sendall(json.dumps('pong').encode(encoding='utf-8'))
        continue

    words = spellchecker.split_words(msg)

    #wrong_indices = []

    # for i in range(len(words)):
    #     if spellchecker.correction(words[i]) != words[i]:
    #         print("{} is wrong. Correct is {}".format(words[i], spellchecker.correction(words[i])))
    #         wrong_indices.append(i)

    wrong_indices = list(spellchecker.unknown(words))
    
    print("Erros encontrados: ", wrong_indices)

    bill = calculate_bill(len(words))

    data = {
        'wrong_words': wrong_indices,
        'bill': bill
    }

    print(data)

    c.send(json.dumps(data).encode(encoding='utf-8'))