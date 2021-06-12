import pygame
from number_sprite import Number

class Resource(pygame.sprite.Sprite):   # class for the Resources of the game
    paths = {"o": "../imgs/ore4.png", "l": "../imgs/lumber4.png", "b": "../imgs/brick1.png", "d": "../imgs/desert1.png",
             "s": "../imgs/sheep1.png", "w": "../imgs/wheat1.png"}
    calcx = 59
    calcy = 78

    def __init__(self, char, num, location, id):    # Initialises Resource in the Game
        pygame.sprite.Sprite.__init__(self)  # as super()
        self.image = pygame.image.load(self.paths[char]).convert_alpha()
        self.rect = self.image.get_rect(topleft=location)
        self.location = location
        self.size = (Resource.calcx, Resource.calcy)
        self.number = num
        self.id = id
        if int(self.number) > 0:     # if number != -1, define a Number for the Resource
            number_location = (location[0] + Resource.calcx / 2, location[1] + Resource.calcy / 2)
            self.number_sprite = Number(num, number_location)
