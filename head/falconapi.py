import falcon, json
from falcon.http_status import HTTPStatus

import socket

class BillGenerator():
    def on_get(self, req, resp):
        resp.body = json.dumps(15)

class Spellcheck():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        data = req.get_param('text')

        s = socket.socket()

        s.connect(('localhost', 12345))

        s.send(data.encode(encoding='utf-8'))

        result = s.recv(1024).decode(encoding='utf-8')

        wrong_indices = json.loads(result)

        print(wrong_indices)

        resp.body = json.dumps(wrong_indices)

class HandleCORS(object):
    def process_request(self, req, resp):
        resp.set_header('Access-Control-Allow-Origin', '*')
        resp.set_header('Access-Control-Allow-Methods', '*')
        resp.set_header('Access-Control-Allow-Headers', '*')
        resp.set_header('Access-Control-Max-Age', 1728000)  # 20 days
        if req.method == 'OPTIONS':
            raise HTTPStatus(falcon.HTTP_200, body='\n')
    
api = falcon.API(middleware=[HandleCORS()])

api.add_route('/bill', BillGenerator())
api.add_route('/spellcheck', Spellcheck())