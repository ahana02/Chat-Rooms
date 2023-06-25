import socket
import threading

nickname = input("Choose your nickname: ")
partner = ""

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 9999))

stop_thread = False


def receive():
    while True:
        if stop_thread:
            break
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'nickname?':
                client.send(nickname.encode('ascii'))
            elif "partners" in message:
                global partner
                partner = message.split(" ")[-1]
                print("Connected to:", partner)
            elif "disconnect" in message:
                partner = ""
            else:
                print(message)
        except:
            print("An error occured!")
            client.close()
            break


def write():
    while True:
        m = input()

        if m.startswith('/chat'):
            global partner
            partner = m.split(" ")[-1]
            mess = '{} partners {}'.format(nickname, partner)
            client.send(mess.encode('ascii'))
            print("Connected to:", partner)
            continue

        if partner == "":
            message = '{}: {} broadcast'.format(nickname, m)
            client.send(message.encode('ascii'))
        else:
            message = '{}: {} {}'.format(nickname, m, partner)
            client.send(message.encode('ascii'))

        if m == 'Bye':
            global stop_thread
            stop_thread = True
            break


receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()