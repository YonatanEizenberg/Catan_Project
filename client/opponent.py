from background import Background


class Opponent:

    def __init__(self, name, id, color, order_id, background_string):            # Initialises Opponent in the Game
        self.name = name
        self.id = id
        self.orderId = order_id
        self.color = color
        self.points = 0
        self.cards = 0
        self.setts = []
        self.roads = []
        self.cities = []
        self.background = Background(background_string)

    def addSett(self, point, resourcesWasted):      # Adds new settlement to the setts list
        self.setts += [point]
        self.points += 1
        if len(self.roads) >= 2:                    # if more than 2 roads than it is the 2nd part of the game
            self.deduct_cards(resourcesWasted)

    def addCity(self, point, resourcesWasted):      # Adds new city to the cities list and remove it from the setts list
        self.setts.remove(point)
        self.cities += [point]
        self.points += 1
        self.deduct_cards(resourcesWasted)

    def deduct_cards(self, resourcesWasted):        # deducts the resources that are given from the self.cards variable
        for resource in resourcesWasted:
            self.cards -= resourcesWasted[resource]

    def display(self, screen, myfont, location, color):    # Displays the data on the screen as a text
        textsurface = myfont.render(self.name, False, color)
        screen.blit(textsurface, location)
        location = (location[0] + 100, location[1])
        for string in [str(self.cards), str(self.points)]:
            textsurface = myfont.render(string, False, color)
            screen.blit(textsurface, location)
            location = (location[0] + 20, location[1])