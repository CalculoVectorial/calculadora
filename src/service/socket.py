import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to the server')

@sio.on('graph')
def on_graph(data):
    print(data)

server_url = 'https://calc-backend-na60.onrender.com'
sio.connect(server_url)

sio.wait()