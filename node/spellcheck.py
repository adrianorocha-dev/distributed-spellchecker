import socket, json
from spellchecker import SpellChecker

s = socket.socket()

s.bind(('', 12345))

s.listen(5)

while(True):
    c, addr = s.accept()

    print('{} connected.'.format(addr))

    msg = c.recv(1024).decode(encoding='utf-8')

    print("received: {}".format(msg))

    spellchecker = SpellChecker()

    in_data = json.loads(msg)

    words = spellchecker.split_words(in_data)

    wrong_indices = []

    for i in range(len(words)):
        if spellchecker.correction(words[i]) != words[i]:
            print("{} is wrong. Correct is {}".format(words[i], spellchecker.correction(words[i])))
            wrong_indices.append(i)
    
    data = {
        'wrong_words': wrong_indices
    }

    c.send(json.dumps(data).encode(encoding='utf-8'))