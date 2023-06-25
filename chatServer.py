import socket
import threading

host = 'localhost'
port = 9999

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(5)

clients = []
nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)


def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            ma = " ".join(message.split(" ")[:-1])
            m_type = message.split(" ")[-1]

            if "partners" in message:
                index = nicknames.index(m_type)
                clientp = clients[index]
                p = message.split(" ")[0]
                ma = 'partners {}'.format(p)
                clientp.send(ma.encode('ascii'))
                continue

            if m_type == "broadcast":
                broadcast(ma.encode('ascii'))
            else:
                print("sent", m_type)
                index = nicknames.index(m_type)
                clientp = clients[index]
                clientp.send(ma.encode('ascii'))

            if 'Bye' in ma:
                clientp.send("disconnect".encode('ascii'))
                print("Me here")
                index = clients.index(client)
                clients.remove(client)
                client.close()
                nickname = nicknames[index]
                broadcast('{} left!'.format(nickname).encode('ascii'))
                nicknames.remove(nickname)
        except:
            client.close()
            break


def receive():
    while True:
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        client.send('nickname?'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print("Nickname is {}".format(nickname))
        broadcast("{} joined!".format(nickname).encode('ascii'))
        client.send('Connected to server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


receive()