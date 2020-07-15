import tornado.ioloop
import tornado.web
import tornado.websocket
from time import time
import json
import matplotlib.pyplot as plt
from IPython import embed
    
do_embed = False
times = []
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html")
    
class SimpleWebSocket(tornado.websocket.WebSocketHandler):
    connections = set()
    
    def open(self):
        self.connections.add(self)
    
    def on_message(self, message):
        message = json.loads(message)
        if message['what'] == 'time':
            message['python_time'] = str(int(time()*1000))
            [client.write_message(message) for client in self.connections]
        else:

            if 'manual' in message['what']:
                # nonsense global stuff bc i couldn't get embed to work from here
                global do_embed
                global times
                do_embed = True
                times = message['times']
            else:
                plt.hist(message['times'], bins='auto', density=True)
                plt.xlabel('round trip (ms)')
                plt.show()
            tornado.ioloop.IOLoop.current().stop()
    
    def on_close(self):
        self.connections.remove(self)
    
def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/websocket", SimpleWebSocket)
    ])
    
if __name__ == "__main__":
    app = make_app()
    app.listen(9999)
    print('http://localhost:9999/')
    tornado.ioloop.IOLoop.current().start()
    if do_embed:
        embed(colors='neutral')