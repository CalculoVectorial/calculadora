import socketio

sio = socketio.Client()

@sio.event
def connect():
    print('Connected to the server')

@sio.on('graph')
def on_graph(data):
    print(data)
    with open('accelerations.csv', 'a') as file:
        file.write(f'{data["x"]},{data["y"]},{data["z"]}\n')

# DEV
# server_url = 'http://localhost:3000'
# PROD
server_url = 'https://calc-backend-na60.onrender.com'
sio.connect(server_url)

sio.wait()