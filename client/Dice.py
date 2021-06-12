import pygame


class Dice(pygame.sprite.Sprite):           # Class for 2 Dices on the PyGame screen
    path = [(673, 366), (727, 366)]         # 2 Screen locations for the 2 Dices
    counter = 0                             # Counter for the dices

    def __init__(self, num):                # Initialises the Dice
        pygame.sprite.Sprite.__init__(self)
        location = self.path[Dice.counter]
        self.image = pygame.image.load(f"../imgs/{num}dice.png").convert_alpha()
        self.rect = self.image.get_rect(center=location)
        Dice.counter += 1

    def update_num(self, num):              # Updates the number on the dice
        self.image = pygame.image.load(f"../imgs/{num}dice.png").convert_alpha()

    def darken_image(self):                 # Darkens the image of the Dice until it is pressed
        dark = pygame.Surface((self.image.get_width(), self.image.get_height()), flags=pygame.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        self.image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)
