import random


class Player:       # A class for each Player

    def __init__(self, name, order, color, id, client_socket):  # Defines the Player
        self.name = name
        self.id = id
        self.order = order
        self.color = color
        self.cards = {"w": 0, "l": 0, "o": 0, "b": 0, "s": 0}
        self.client_socket = client_socket
        self.points = 0
        self.sett_points = []
        self.city_points = []
        self.roads = []
        self.new_earnings = {"w": 0, "l": 0, "o": 0, "b": 0, "s": 0}

    def get_message(self):      # returns the message for the player
        return f"{self.id}:{self.name}:{self.color}"

    def add_sett_point(self, point, points_object):     # Adds settlement point to the player
        self.sett_points += [point]
        self.points += 1
        response = points_object.buildStatus(point, self.id)
        return response

    def calculateEarnings(self, sum):       # calculates earnings by the given sum
        for point in self.sett_points:
            for resource in point.resources:
                if int(resource.number) == sum:
                    self.new_earnings[resource.char] += 1
        for point in self.city_points:
            for resource in point.resources:
                if int(resource.number) == sum:
                    self.new_earnings[resource.char] += 2

    def strGot(self):      # returns str of the earnings
        got = []
        for earningChar in self.new_earnings:
            earnings = self.new_earnings[earningChar]
            if earnings != 0:
                got += [f"{earningChar}{earnings}"]
        return ",".join(got)

    def resetNewEarnings(self):     # resets the new earnings dictionary
        for earningChar in self.new_earnings:
            if self.new_earnings[earningChar] != 0:
                self.cards[earningChar] += self.new_earnings[earningChar]
                self.new_earnings[earningChar] = 0

    def newCity(self, point):       # Builds new city
        self.sett_points.remove(point)
        self.city_points += [point]
        self.points += 1