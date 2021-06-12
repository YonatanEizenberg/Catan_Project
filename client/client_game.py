""" With map and player"""
import time
from pygame.locals import *
import os
from Button import Button
from Dice import Dice
from Resource import *
from Player import Player
from roadsSetter import setRoads
from opponent import Opponent
import tcp_client
from pointsSetter import setPoints
from resourcesSetter import setResources
import audio_client
import threading
import keyboard


class Game:  # The class to deal with responses from the server
    # class variables, revoke with 'self.' or 'Game.'
    width = 900
    height = 500
    xy = [(100, 100), (400, 50)]

    def __init__(self):  # Initialises all the objects
        """ declare all game objects (as in constructor)"""
        self.running = False
        self.screen = None
        self.sprites_group = None  # group of static and movable game objects
        self.end_turn_sprite = None
        self.road_button = None
        self.sett_button = None
        self.points_object = None
        self.roads_object = None
        self.on_init()
        self.name = ""
        self.player = None
        self.opponents = []
        self.map = None
        self.resources = []
        self.settPointsToBuild = []
        self.roadsToBuild = []
        self.cityPointsToBuild = []
        self.clicked_sprite = None
        self.message = None
        self.my_turn = False
        self.buildRoad = False
        self.settsBuilt = []
        self.clicked_dice = False
        self.clicked_Button = False
        self.audio_client = None
        self.all_players = []
        self.req_build = {"r": {"l": 1, "b": 1}, "s": {"l": 1, "b": 1, "s": 1, "w": 1}, "c": {"w": 2, "o": 3}}
        self.display_locations = [(770, 112), (770, 162), (770, 212)]
        self.color_data = {"red": (255, 0, 0), "blue": (0, 0, 255), "green": (0, 255, 0)}
        self.tcp_client = tcp_client.ConnectAndSend(self)

    def on_init(self):
        """ all game objects initialization"""

        # set title
        pygame.display.set_caption("Catan Game")
        self.screen = pygame.display.set_mode((Game.width, Game.height))
        self.sprites_group = pygame.sprite.Group()
        self.end_turn_sprite = Button("a")
        self.sprites_group.add(self.end_turn_sprite)
        self.road_button = Button("r")
        self.sprites_group.add(self.road_button)
        self.sett_button = Button("s")
        self.sprites_group.add(self.sett_button)
        self.city_button = Button("c")
        self.sprites_group.add(self.city_button)
        self.dice1 = Dice("1")
        self.dice2 = Dice("1")
        self.sprites_group.add(self.dice1)
        self.sprites_group.add(self.dice2)
        self.build_costs_button = Button("b")
        self.sprites_group.add(self.build_costs_button)

    def use_data_from_tcp(self, response_str):  # handles with the data from server
        msg = response_str.strip()
        self.message = msg
        if msg.startswith("Wait to start"):
            self.id = int(msg.split(":")[1])
            self.name = input("Enter Name:")
            self.tcp_client.send(str(self.id) + "name:" + self.name)
            self.audio_client = audio_client.Audio_Client()
            threading.Thread(target=self.audio_client.receive_server_data).start()

        elif msg.startswith("select_color:"):
            order, colors = msg.split(":")
            all_colors = colors.split(",")
            while True:
                for color in all_colors:
                    if color == "r":
                        print("For the color Red Enter 'R'")
                    elif color == "b":
                        print("For the color Blue Enter 'B'")
                    elif color == "g":
                        print("For the color Green Enter 'G'")
                c = input("Enter Color:")
                if c in all_colors:
                    break
            self.tcp_client.send(f"select_color:{c.lower()}")

        elif msg == "Bye":
            self.running = False

        elif msg.startswith("board"):
            msg = msg[5::]
            msg_list = msg.split(",")
            print(msg_list)
            print(self.sprites_group)
            self.map = setResources(msg_list, self.sprites_group, self.resources)
            self.points_object = setPoints(self.resources)
            self.setSettsToBuild()
            self.roads_object = setRoads(self.settPointsToBuild)

        elif msg.startswith("players"):
            msg = msg[7::]
            msg = msg[1:-1:]
            msg_list = msg.split(",")
            order_id = 0
            for msg in msg_list:
                print(msg)
                if msg != "":
                    id, name, color = msg.split(":")
                    if name == self.name:
                        self.player = Player(name, int(id), color, order_id, self.display_locations[order_id])
                        self.sprites_group.add(self.player.background)
                    else:
                        self.opponents += [Opponent(name, int(id), color, order_id, self.display_locations[order_id])]
                        self.sprites_group.add(self.opponents[-1].background)
                order_id += 1
            self.all_players = [self.player] + self.opponents
            print(self.player.__str__())

        elif msg.startswith("start_build_sett:"):
            for p in self.all_players:
                p.background.brighten_image()
            user_id = msg[17::]
            if int(user_id) == self.id:
                self.my_turn = True
                self.setSettsToBuild()
                pointsToShow(self.sprites_group, self.settPointsToBuild)

            else:
                opp = find_player(self.opponents, user_id)

            for p in self.all_players:
                if p.id == int(user_id):
                    p.background.darken_image()

        elif msg.startswith("build_sett"):
            order, id, pointBuildId, pointsId = msg.split(":")
            if str(self.id) != id:
                opp = find_player(self.opponents, id)
                pointBuild = self.points_object.find_point(pointBuildId)
                pointBuild.build(self.sprites_group, self.settPointsToBuild, self.settsBuilt, opp.color)
                opp.addSett(pointBuild, self.req_build["s"])
            pointsIdArray = pointsId.split(",")
            for pointId in pointsIdArray:
                point = self.points_object.find_point(pointId)
                point.setBuildFalse(self.sprites_group, self.settPointsToBuild)

        elif msg.startswith("start_build_road"):
            self.setRoadsToBuild()
            pointsToShow(self.sprites_group, self.roadsToBuild)

        elif msg.startswith("build_road"):
            order, id, roadId, pointId = msg.split(":")
            if str(self.id) != id:
                player = find_player(self.opponents, id)
                road = self.roads_object.find_road(roadId, pointId)
                player.roads += [road]
                road.build_opp(self.sprites_group, player.color)
                self.sprites_group.remove(self.settsBuilt)
                self.sprites_group.add(self.settsBuilt)

                if len(player.roads) > 2:
                    player.deduct_cards(self.req_build["r"])

        elif msg.__contains__("got:"):
            if int(msg[0]) == self.id:
                message = msg.split(":")
                if message[1]:
                    for data in message[1].split(","):
                        char = data[0]
                        number = int(data[1::])
                        print(f"got {number} of {char}")
                        self.player.cards[char] += number
                if len(message) > 2:
                    for data in message[2].split(","):
                        oppId = int(data[0])
                        sum = int(data[1::])
                        opp = find_player(self.opponents, oppId)
                        opp.cards += sum
                if self.my_turn and len(self.player.roads) >= 2:
                    self.check_buttons()
            else:
                oppId = int(msg[0])
                sum = int(msg.split(":")[1])
                opp = find_player(self.opponents, oppId)
                print(f"{opp.name} got {sum} cards")
                opp.cards += sum

        elif msg.startswith("turn:"):
            for p in self.all_players:
                p.background.brighten_image()
            msg = msg[5::]
            id = msg[0]
            if int(id) == self.id:
                self.my_turn = True
                self.clicked_Button = False
                self.clicked_dice = False
                self.dice1.darken_image()
                self.dice2.darken_image()
            for p in self.all_players:
                if p.id == int(id):
                    p.background.darken_image()
                else:
                    p.background.brighten_image()

        elif msg.startswith("dice:"):
            order, num1, num2 = msg.split(":")
            print(f"dices: {num1}, {num2}, sum {int(num1) + int(num2)}")
            self.dice1.update_num(num1)
            self.dice2.update_num(num2)
            if self.my_turn:
                self.clicked_dice = True
            if int(num1) + int(num2) == 7 and self.my_turn:
                self.check_buttons()

        elif msg.__contains__("upgrade:"):
            id_order, pointId = msg.split(":")
            playerId = id_order[0]
            if int(playerId) != self.id:
                opp = find_player(self.opponents, playerId)
                point = self.points_object.find_point(pointId)
                point.show_image("city", self.sprites_group)
                opp.addCity(point, self.req_build["c"])

    def on_event(self, event):  # Deals with all events
        """ callback after events """
        if event.type == QUIT:
            if self.tcp_client:
                self.tcp_client.send("".join(["3", "Bye"]))
            self.running = False

        # handle a mouse press
        elif event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            self.clicked_sprite = None
            for s in self.sprites_group:
                if s.rect.collidepoint(pos):
                    self.clicked_sprite = s
                    self.deal_click()
        else:
            if keyboard.is_pressed('v') and self.audio_client:
                threading.Thread(target=self.audio_client.send_data_to_server).start()
            finished_game = False
            string = ""
            if self.player and self.opponents:
                if self.player.points >= 10:
                    string = "You Won!"
                    finished_game = True
                for opp in self.opponents:
                    if opp.points >= 10:
                        string = "You Lost ):"
                        finished_game = True
                if finished_game:
                    data_font = pygame.font.SysFont('David', 50)
                    textsurface = data_font.render(self.name, False, (0, 0, 0))
                    self.screen.blit(textsurface, (280, 136))
                    time.sleep(2)
                    if self.tcp_client:
                        self.tcp_client.send("".join(["3", "Bye"]))
                    self.running = False

    def on_update(self):        # updates the sprites display
        """ update all game objects"""
        pygame.display.update()
        self.sprites_group.update()

    def on_render(self):        # Rendering the sprites
        """ draw all game objects"""

        frame = pygame.image.load("../imgs/frame4.jpg")
        self.screen.blit(frame, (0, 0))
        self.sprites_group.draw(self.screen)

        pygame.font.init()
        data_font = pygame.font.SysFont('David', 20)
        cards_font = pygame.font.SysFont('David', 33)
        if self.player and self.opponents:
            self.all_players.sort(key=lambda x: x.orderId)
            location = (700, 100)
            for player in self.all_players:
                if isinstance(player, Player):
                    player.display(self.screen, data_font, cards_font, location, self.color_data[player.color])
                else:
                    player.display(self.screen, data_font, location, self.color_data[player.color])
                location = (location[0], location[1] + 50)

    def on_execute(self):   # The endless animation loop
        """ animation loop"""

        self.running = True
        while self.running:

            # reacts on events *****************************************
            for event in pygame.event.get():
                self.on_event(event)

            # update data **********************************************
            self.on_update()

            # drawing **************************************************
            self.on_render()

            # time in milliseconds for watch the screen ****************
            pygame.time.delay(100)

        pygame.quit()

    def deal_click(self):       # deals with the click on the scremm
        if self.clicked_sprite in self.settPointsToBuild:
            if self.clicked_sprite.canBuild:
                self.clicked_sprite.build(self.sprites_group, self.settPointsToBuild, self.settsBuilt,
                                          self.player.color)
                self.player.addSett(self.clicked_sprite)
                mes = f"build_sett:{self.id}:{self.clicked_sprite.id}"
                self.tcp_client.send(mes)

                if len(self.player.roads) >= 2:
                    self.player.deduct_cards(self.req_build["s"])
                    self.check_buttons()

            removePoints(self.sprites_group, self.settPointsToBuild)

        elif self.clicked_sprite in self.roadsToBuild:
            if self.clicked_sprite.canBuild:
                print("build a road")
                mes = f"build_road:{self.id}:{self.clicked_sprite.id}:{self.clicked_sprite.pointsId[0]}"
                print(mes)
                self.tcp_client.send(mes)
                self.clicked_sprite.build(self.sprites_group, self.roadsToBuild, self.player.color)
                self.player.roads += [self.clicked_sprite]
                self.sprites_group.remove(self.settsBuilt)
                self.sprites_group.add(self.settsBuilt)

                print(f"road's location: ({self.clicked_sprite.location[0]}, {self.clicked_sprite.location[1]})")
                print(f"points Ids near road: {self.clicked_sprite.pointsId[0]}, {self.clicked_sprite.pointsId[1]}")

                if len(self.player.roads) <= 2:
                    removePoints(self.sprites_group, self.roadsToBuild)
                    mes = "finished_turn"
                    # self.player.background.brighten_image()
                    print(mes)
                    self.tcp_client.send(mes)
                    self.my_turn = False

                else:
                    self.player.deduct_cards(self.req_build["r"])
                    self.check_buttons()

        elif self.clicked_sprite in self.cityPointsToBuild:
            point = self.clicked_sprite
            point.show_image("city", self.sprites_group)
            self.player.addCity(point, self.req_build["c"])
            self.cityPointsToBuild.remove(point)
            self.tcp_client.send(f"{self.id}upgrade:{point.id}")
            for point in self.cityPointsToBuild:
                point.show_image("sett", self.sprites_group)
            self.check_buttons()

        elif self.clicked_sprite == self.dice1 or self.clicked_sprite == self.dice2:
            if self.my_turn and not self.clicked_dice:
                self.clicked_dice = True
                self.tcp_client.send("dice")

        elif self.my_turn and self.clicked_sprite and self.player.points >= 2:
            if self.clicked_Button:
                if self.roadsToBuild in self.sprites_group:
                    removePoints(self.sprites_group, self.roadsToBuild)
                elif self.settPointsToBuild in self.sprites_group:
                    removePoints(self.sprites_group, self.settPointsToBuild)

            if self.clicked_sprite == self.road_button and self.road_button.canBuild:
                self.setRoadsToBuild()
                pointsToShow(self.sprites_group, self.roadsToBuild)
                self.clicked_Button = True

            elif self.clicked_sprite == self.sett_button and self.sett_button.canBuild:
                self.setSettsToBuild()
                pointsToShow(self.sprites_group, self.settPointsToBuild)
                self.clicked_Button = True

            elif self.clicked_sprite == self.city_button and self.city_button.canBuild:
                self.setCitiesToBuild()
                self.clicked_Button = True

            elif self.clicked_sprite == self.end_turn_sprite:
                # if self.my_turn and self.clicked_dice:
                self.my_turn = False
                self.clicked_dice = False
                self.tcp_client.send("finished_turn")
                for button in [self.road_button, self.sett_button, self.city_button]:
                    if not button.canBuild:
                        button.can_build()

    def setRoadsToBuild(self):      # Defines the roads that are available to build on
        self.roadsToBuild = []
        p = self.player
        if len(p.roads) < 2:
            point = p.setts[-1]
            for road in point.roads:
                if road.canBuild:
                    self.roadsToBuild += [road]
        else:
            print(f"number of roads is {len(p.roads)}")
            for road in p.roads:
                self.roadsToBuild += self.roads_object.find_close_available_roads(road)

    def setSettsToBuild(self):      # Defines the settlements that are available to build on
        self.settPointsToBuild = []
        p = self.player
        if p.points < 2:
            for point in self.points_object.returnValues():
                if point.canBuild:
                    self.settPointsToBuild += [point]
        else:
            for road in p.roads:
                setts = road.find_close_available_points(self.points_object.returnValues())
                self.settPointsToBuild += [sett for sett in setts if sett not in self.settPointsToBuild]

    def setCitiesToBuild(self):     # Defines the cities that are available to build on
        self.cityPointsToBuild = []
        p = self.player
        for sett in p.setts:
            sett.show_image("circle", self.sprites_group)
            self.cityPointsToBuild += [sett]

    def check_buttons(self):        # check all the buttons of the game and if they can be pressed
        button_dict = {"r": self.road_button, "s": self.sett_button, "c": self.city_button}
        for char in button_dict:
            for resource in self.req_build[char]:
                button = button_dict[char]
                if button.canBuild and self.req_build[char][resource] > self.player.cards[resource]:
                    button.cannot_build()
                    continue


def pointsToShow(sprites, pointsToAdd):     # adds the pointsToAdd to the sprites group
    sprites.add(pointsToAdd)


def removePoints(sprites, points):          # Removes the points from sprites if they are in the sprites
    for point in points:
        if point in sprites:
            sprites.remove(point)


def find_player(players, playerId):         # Finds the player by the given playerId
    for player in players:
        if player.id == int(playerId):
            return player


def main():         # main function that executes the game
    pygame.init()
    # set pygame screen location
    os.environ['SDL_VIDEO_WINDOW_POS'] = "{},{}".format(100, 100)
    my_game = Game()
    my_game.on_execute()


if __name__ == "__main__":
    main()
