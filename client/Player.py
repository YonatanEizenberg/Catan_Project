from background import Background


class Player:

    def __init__(self, name, id, color, order_id, background_string):            # Initialises Opponent in the Game
        self.name = name
        self.id = id
        self.orderId = order_id
        self.color = color
        self.points = 0
        self.cards = {"l": 0, "b": 0, "s": 0, "w": 0, "o": 0}
        self.card_l_location = (13, 442)
        self.cards_location_gap = 65
        self.setts = []
        self.roads = []
        self.cities = []
        self.background = Background(background_string)

    def addSett(self, point):                       # Adds new settlement to the setts list
        self.setts += [point]
        self.points += 1

    def addCity(self, point, resourcesWasted):      # Adds new city to the cities list and remove it from the setts list
        self.setts.remove(point)
        self.cities += [point]
        self.points += 1
        self.deduct_cards(resourcesWasted)

    def deduct_cards(self, resourcesWasted):        # deducts the resources that are given from the self.cards variable
        for resource in resourcesWasted:
            self.cards[resource] -= resourcesWasted[resource]

    def display(self, screen, data_font, cards_font, data_location, color):              # Displays the data on the screen as a text
        location = self.card_l_location
        for char in self.cards:                     # Data about the Cards
            string = str(self.cards[char])
            textsurface = cards_font.render(string, False, (0, 0, 0))
            screen.blit(textsurface, location)
            location = (location[0] + self.cards_location_gap, location[1])

        sumcards = 0
        location = data_location
        for num in self.cards.values():
            sumcards += num
        textsurface = data_font.render(self.name, False, color)
        screen.blit(textsurface, location)
        location = (location[0] + 100, location[1])
        for string in [str(sumcards), str(self.points)]:         # Data about the Player
            textsurface = data_font.render(string, False, color)
            screen.blit(textsurface, location)
            location = (location[0] + 20, location[1])

    def cards_sum(self):
        sum = 0
        for num in list(self.cards.values()):
            sum += num
        return sum