import pygame


class Button(pygame.sprite.Sprite):         # class for Buttons on the PyGame screen
    # dictionary that contains the location and image path of objects by char
    # a = arrows for the end of the turn, r = Road Button, s= Settlement Button, c = City Button
    paths = {"a": [(838, 436), "../imgs/arrow1.png"], "r": [(658, 436), "../imgs/road5.png"],
             "s": [(718, 436), "../imgs/set1.png"], "c": [(778, 436), "../imgs/city2.png"],
             "b": [(107, 222), "../imgs/build_costs.jpg"], "back0": [(770, 112), "../imgs/data_background.png"],
             "back1": [(770, 162), "../imgs/data_background.png"], "back2": [(770, 212), "../imgs/data_background.png"]}

    def __init__(self, char):               # initialises the Button Object
        pygame.sprite.Sprite.__init__(self)
        location, self.image_path = self.paths[char]
        self.image = pygame.image.load(self.image_path).convert_alpha()
        self.rect = self.image.get_rect(center=location)
        self.canBuild = True

    def cannot_build(self):                 # changes the Button's variables to can't build
        self.canBuild = False
        dark = pygame.Surface((self.image.get_width(), self.image.get_height()), flags=pygame.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        self.image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def can_build(self):                    # changes the Button's variables to can build
        self.canBuild = True
        self.image = pygame.image.load(self.image_path).convert_alpha()
