import socket
import threading

#server connection data
host=socket.gethostbyname(socket.gethostname())
port=1050

#starting server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind((host,port))
s.listen()
print("Server is listening on {}".format(str(host)))

#list of clients and nicknames
clients=[]
nicknames=[]

#sending message to all connected clients
def broadcast(message):
    for client in clients:
        client.send(message)

#handling clients
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            message = '{} has left the chat'.format(nickname).encode('ascii')
            broadcast(message)
            nicknames.remove(nickname)
            break

#receiving and listentin
def receive():
    while True:
        client,address = s.accept()
        print('Connection from {}'.format(str(address)))

        client.send('Nick'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        broadcast('{} has joined!'.format(nickname).encode('ascii'))
        client.send('Connected to server at {}'.format(host).encode('ascii'))

        thread = threading.Thread(target=handle,args=(client,))
        thread.start()

receive()
