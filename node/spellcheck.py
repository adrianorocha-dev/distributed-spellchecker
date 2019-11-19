import socket, json
from spellchecker import SpellChecker
import time

from sjcl import SJCL

sjcl = SJCL()

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

def decode_cipher_dict(cipher_dict):
    for k, v in cipher_dict.items():
        if type(v) == bytes:
            cipher_dict[k] = v.decode()
    
    return cipher_dict

connect_to_head()

s = socket.socket()

s.bind(('', 12345))

s.listen(5)

spellchecker = SpellChecker()

while(True):
    print('Waiting for connection')
    c, addr = s.accept()

    print('{} connected.'.format(addr))

    msg = b''

    while True:
        b = c.recv(4096)
        msg += b
        if len(b) < 4096:
            break
    
    msg = msg.decode(encoding='utf-8')
    print('Message to received: ', msg)
    
    if msg == 'ping':
        c.sendall(json.dumps('pong').encode(encoding='utf-8'))
        continue

    msg = json.loads(msg)

    msg = sjcl.decrypt(msg, config['crypto_key']).decode()

    print("received: {}".format(msg))

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

    cipher_data = decode_cipher_dict(sjcl.encrypt(json.dumps(data).encode(), config['crypto_key']))
    print(cipher_data)

    c.sendall(json.dumps(cipher_data).encode('utf-8'))