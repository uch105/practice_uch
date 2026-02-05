import socket
import threading

nickname = input('Choose a nickname: ')

client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.56.1',1050))

#listening to server
def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'Nick':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print('An error occured')
            client.close()
            break

def write():
    while True:
        message = '{} : {}'.format(nickname,input(''))
        client.send(message.encode('ascii'))

recv_thread = threading.Thread(target=receive)
recv_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()