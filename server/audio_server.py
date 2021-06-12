import threading
import socket
from my_constants import *


class Audio_Server:         # sets the Audio server

    def __init__(self):
        self.ip = IP
        while 1:
            try:
                self.port = TCP_PORT_NUMBER + 1

                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.s.bind((self.ip, self.port))

                break
            except:
                print("Couldn't bind to that port")

        self.connections = []
        threading.Thread(target=self.accept_connections).start()

    def accept_connections(self):           # Accepts new connections
        self.s.listen(100)

        print('Running Audio on IP: ' + self.ip)
        print('Running Audio on port: ' + str(self.port))

        while len(self.connections) <= NUM_OF_CLIENTS:
            c, addr = self.s.accept()
            threading.Thread(target=self.handle_client, args=(c, addr,)).start()
            self.connections.append(c)

    def broadcast(self, sock, data):        # Broadcasts the data to all the players
        sent_addresses = []
        for client in self.connections:
            if client != self.s and client != sock:
                try:
                    client.send(data)
                except:
                    pass

    def handle_client(self, c, addr):       # Receives data from client and broadcasts it
        while 1:
            try:
                data = c.recv(1024)
                self.broadcast(c, data)

            except socket.error:
                c.close()
