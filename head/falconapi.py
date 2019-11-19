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

        data = sjcl.decrypt(data, '12345').decode()

        # removing disconnected nodes
        verify_available_nodes()

        if len(nodes) < 1:
            result_data = { 'wrong_words': [], 'bill': 0, 'errors': ["Nenhum nó de processamento disponível."] }
            
            result_data = decode_cipher_dict( sjcl.encrypt(json.dumps(result_data).encode(), '12345') )
            resp.body = json.dumps(result_data)
            return

        # Balanceamento
        total_latency = sum([node.latency for node in nodes])

        node_percentage = [node.latency / total_latency for node in nodes]
        node_percentage.reverse()

        words = data.split(' ')


        print("dividing {} words to {} nodes".format(len(words), len(nodes)))
        n_words_per_node = len(words) // len(nodes)
        print("sending {} words to each node".format(n_words_per_node))

        wrong_words = []
        bill = 0

        for i in range(len(nodes)):
            if i < len(nodes)-1 :
                msg_split = ' '.join(words[i*n_words_per_node:(i+1)*n_words_per_node])
            else:
                msg_split = ' '.join(words[i*n_words_per_node:])

            s = socket.socket()

            s.connect((nodes[i].ip, config['port']))

            print('Connected to node, sending data...')

            cipher_msg = decode_cipher_dict( sjcl.encrypt(msg_split.encode(), '12345') )
            print(cipher_msg)
            s.sendall(json.dumps(cipher_msg).encode('utf-8'))

            print('waiting for response...')

            result = s.recv(1024).decode(encoding='utf-8')
            result = json.loads(result)

            result = json.loads(sjcl.decrypt(result, '12345'))

            wrong_words += result['wrong_words']
            bill += result['bill']
        
        result_data = {
            'wrong_words': wrong_words,
            'bill': bill
        }

        result_data = decode_cipher_dict( sjcl.encrypt(json.dumps(result_data).encode(), '12345') )

        print("Sending result: ", result_data)
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