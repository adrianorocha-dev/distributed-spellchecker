import falcon, json

import socket

class BillGenerator():
    def on_get(self, req, resp):
        resp.body = json.dumps(15)

class Spellcheck():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())

        s = socket.socket()

        s.connect('localhost', 12345)

        s.send(json.dumps(data).encode(encoding='utf-8'))

        result = s.recv(1024).decode(encoding='utf-8')

        wrong_indices = json.loads(result)

        print(wrong_indices)

        resp.body = json.dumps(data)
    
api = falcon.API()

api.add_route('/bill', BillGenerator())
api.add_route('/spellcheck', Spellcheck())