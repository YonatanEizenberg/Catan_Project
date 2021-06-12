import pygame


class Background(pygame.sprite.Sprite):         # class for Buttons on the PyGame screen
    path = "../imgs/background.png"

    def __init__(self, location):               # initialises the Button Object
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(Background.path).convert_alpha()
        self.rect = self.image.get_rect(center=location)

    def darken_image(self):                 # changes the Button's variables to can't build
        dark = pygame.Surface((self.image.get_width(), self.image.get_height()), flags=pygame.SRCALPHA)
        dark.fill((50, 50, 50, 0))
        self.image.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

    def brighten_image(self):                    # changes the Button's variables to can build
        self.image = pygame.image.load(Background.path).convert_alpha()
