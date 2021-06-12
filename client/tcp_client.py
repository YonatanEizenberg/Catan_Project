import socket
import threading


class ConnectAndSend():             # The class is responsible for the connection with the server
    def __init__(self, game):
        # Connect to the server:
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect(("127.0.0.1", 12344))
        # Start reading from server in separate thread
        ReadThread(self.client_socket, game).start()    # Starts Threaded Class

    def send(self, request_str):    # Sends the given string to the server after encoding it
        # Send some messages:
        print("in send", request_str)
        request_str = request_str.strip()
        message = "".join([str(len(request_str)).zfill(4),request_str])
        message = message.encode()
        self.client_socket.send(message)


class ReadThread(threading.Thread):     # The class is doing a Thread on receiving data from the server

    def __init__(self, client_socket, game):
        self.client_socket = client_socket
        self.game = game
        threading.Thread.__init__(self)     # starts the Thread that is the run function

    def run(self):                      # endless loop that is receiving data from the server and forward it to the
        try:                            # client to respond to it
            while True:
                response_len = self.client_socket.recv(4).strip()
                msg_len = int(response_len)
                response = self.client_socket.recv(msg_len).strip()
                request_str = response.decode()
                print("got from server", request_str, "|")
                self.game.use_data_from_tcp(request_str)
                if request_str == "Bye":
                    print("break")
                    break

        except Exception as e:
            print("4:", e)

        finally:
            self.client_socket.close()

