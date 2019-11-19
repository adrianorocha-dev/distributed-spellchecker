import falcon, json
from falcon.http_status import HTTPStatus
#from falcon import media
import socket
import threading
import time

from sjcl import SJCL

sjcl = SJCL()

config = json.loads(open('config.json').read())
print('loaded config: ', config)

# Class to take care of the nodes
class Node():
    def __init__(self, s_client, ip):
        super().__init__()
        self.s_client = s_client
        self.ip = ip
        
        self.latency = None
        self.cpu_usage = None
    
    def __eq__(self, value):
        return self.ip == value.ip

# Function to listen to new nodes that want to offer processing
def listen_for_nodes(node_list, port):
    server = socket.socket()
    server.bind(('', port))
    server.listen(5)

    while True:
        c, addr = server.accept()

        node = Node(c, addr[0])

        if node in nodes:
            return

        print("Node {} registered itself.".format(node.ip))
        
        msg = node.s_client.recv(1024).decode(encoding='utf-8')

        if msg == 'connect':
            node_list.append(node)
        
        c.close()

def decode_cipher_dict(cipher_dict):
    for k, v in cipher_dict.items():
        if type(v) == bytes:
            cipher_dict[k] = v.decode()
    
    return cipher_dict

nodes = []

# Creating socket server so nodes can add themselves to the head.
node_listen_thread = threading.Thread(target=listen_for_nodes, args=(nodes, config['listen_port']))
node_listen_thread.start()

# Function to verify if nodes are still connected
def verify_available_nodes():
    global nodes

    for node in nodes:
        try:
            connection = socket.socket()
            print(node.ip)
            connection.connect((node.ip, config['port']))
            connection.send('ping'.encode(encoding='utf-8'))
            
            start = time.time_ns()
            r = connection.recv(1024)
            end = time.time_ns()

            connection.close()

            node.latency = end - start
        except:
            nodes.remove(node)

class Spellcheck():
    
    def on_post(self, req, resp):
        global nodes

        resp.status = falcon.HTTP_200
        #data = req.bounded_stream.read()

        data = req.media.get('text')

        print(data)

        data = json.loads(data)

        data = sjcl.decrypt(data, config['crypto_key']).decode()

        # removing disconnected nodes
        verify_available_nodes()

        if len(nodes) < 1:
            result_data = { 'wrong_words': [], 'bill': 0, 'errors': ["Nenhum nó de processamento disponível."] }
            resp.body = json.dumps(result_data)
            return

        # Balanceamento
        total_latency = sum([node.latency for node in nodes])

        node_percentage = [node.latency / total_latency for node in nodes]
        node_percentage.reverse()

        print('Total percentage:', sum(node_percentage))

        words = data.split(' ')

        wrong_words = []
        bill = 0

        _start = 0
        for i in range(len(nodes)):

            _end = _start + node_percentage[i] * len(words)
            msg_split = ' '.join(words[int(_start):int(_end)])
            print("Sending %.2f of the words (%d words)" % (node_percentage[i], int(_end-_start)))

            s = socket.socket()

            s.connect((nodes[i].ip, config['port']))

            print('Connected to node, sending data...')

            cipher_msg = decode_cipher_dict( sjcl.encrypt(msg_split.encode(), config['crypto_key']) )
            print(cipher_msg)
            s.sendall(json.dumps(cipher_msg).encode('utf-8'))

            print('waiting for response...')

            result = s.recv(1024).decode(encoding='utf-8')
            result = json.loads(result)

            result = json.loads(sjcl.decrypt(result, config['crypto_key']))

            wrong_words += result['wrong_words']
            bill += result['bill']
        
        result_data = {
            'wrong_words': wrong_words,
            'bill': bill
        }

        resp.body = json.dumps(result_data)

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')
    
api = falcon.API(middleware=[HandleCORS()])

api.add_route('/spellcheck', Spellcheck())