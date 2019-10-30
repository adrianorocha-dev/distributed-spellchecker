import falcon, json

class BillGenerator():
    def on_get(self, req, resp):
        resp.body = json.dumps(15)

class Spellcheck():
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        data = json.loads(req.stream.read())

        resp.body = json.dumps(data)
    
api = falcon.API()

api.add_route('/bill', BillGenerator())
api.add_route('/spellcheck', Spellcheck())