
import time
import json
import threading
import random
from my_constants import *


class Game(threading.Thread):
    """
    responsible for sending data to clients.
    That data is checked in many functions.
    fields definition:
    """
    # overriding of constructor
    def __init__(self, sockets_for_animation, message):
        threading.Thread.__init__(self)
        self.sockets_for_animation = sockets_for_animation
        self.game_on = False
        self.message = message
        self.private_message = {}
        self.board = []
        self.users = None


    def run(self):
        """
        Overriding of Thread run method.
        Includes implementation of protocol between server/client
        Output loop- send data to clients in accordance with the game board
        """
        self.game_on = True
        resp = "start"     # "start" consist of 5 chars
        time.sleep(2) # for client get "start"
        i = 0
        while self.game_on:
            time.sleep(SPEED)
            if self.message:
                resp = self.message
                self.send_to_all_clients(resp)
                i = i + 1
        print("end game")

    def send_to_all_clients(self, response_str):
        """
        Sends message  to all players
        response_str: the string to send
        """
        response_str = "".join([str(len(response_str)).zfill(NUMBER_LENGTH), response_str])
        print("send to all", response_str)

        for sock in self.sockets_for_animation:
            response = response_str.encode()
            if self.game_on:
                sock.send(response)

    def update(self, data):
        """
        update data for players
        data: new data
        """
        if data == "Bye":
            self.game_on = False
            resp = "Bye"
            self.send_to_all_clients(resp)
        else:
            self.message = data

    def send_private_message(self, socket, message):        # sends private message to the given socket
        response_str = "".join([str(len(message)).zfill(NUMBER_LENGTH), message])
        if self.game_on:
            socket.send(response_str.encode())

