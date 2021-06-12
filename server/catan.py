import random
from road import *
from player import Player
from resource import *
from point import *


class Catan:  # The Class for the game logic

    def __init__(self):
        self.players = []
        self.points_object = None
        self.resources_object = None
        self.roads_list = None

    def set_order(self, tmp_users):  # Sets the order of players
        new_users = {}
        new_keys = list(tmp_users.keys())
        random.shuffle(new_keys)
        order = 0
        for key in new_keys:
            new_users[key] = tmp_users[key]
        for name in new_users:
            id, color, client_socket = new_users[name]
            p = Player(name, order, color, id, client_socket)
            self.players += [p]
            order += 1

    def set_board(self):  # sets the board by String consists of chars - kind of resource,
        # numbers - the number on the resource
        # s = sheep, o = Ore, b = Brick, w = wheat, l = Lumber, d = Desert
        board_resc = ["s"] * 4 + ["o"] * 3 + ["b"] * 3 + ["w"] * 4 + ["l"] * 4 + ["d"] * 1
        random.shuffle(board_resc)

        board_num = ["2"] + ["3"] * 2 + ["4"] * 2 + ["5"] * 2 + ["6"] * 2 + ["8"] * 2 + ["9"] * 2 + ["10"] * 2 + [
            "11"] * 2 + ["12"]
        random.shuffle(board_num)

        num_counter = 0
        resc_counter = 0
        board_order = []
        for i in range(len(board_resc)):
            if board_resc[resc_counter] != "d":
                num = board_num[num_counter]
                res = board_resc[resc_counter]
                board_order += [res + num]
                num_counter += 1
            else:
                num = -1
                res = "d"
                board_order += ["d-1"]
            resc_counter += 1

        self.resources_object = set_resources(board_order)
        self.points_object = setPoints(self.resources_object.resources)
        self.roads_list = setRoads(list(self.points_object.pointsArray.values())).roads
        return board_order

    def find_player(self, id):      # Finds player by the given ID
        for player in self.players:
            if id == player.id:
                return player
        return None

    def find_road(self, id, pointId):       # Finds road by the given road ID
        for road in self.roads_list:
            if str(road.id) == id:
                for pId in road.pointsId:
                    if str(pId) == pointId:
                        return road
        return None

    def dice(self):         # Randomises the result of the dices
        return random.randrange(1, 7, 1), random.randrange(1, 7, 1)

    def getResponse(self, sum):     # builds the response for each client
        responses = []
        for player in self.players:
            player.calculateEarnings(sum)
        for player in self.players:
            response = f"{player.id}got:"
            response += player.strGot() + ":"
            opponentsGot = []
            for p in self.players:
                if p != player:
                    opponentsGot += [f"{p.id}{sumValues(list(p.new_earnings.values()))}"]
            response += ",".join(opponentsGot)
            responses += [response]
        for player in self.players:
            player.resetNewEarnings()
        return responses


def sumValues(values):      # Sums the num of values list
    sum = 0
    for num in values:
        sum += num
    return sum
