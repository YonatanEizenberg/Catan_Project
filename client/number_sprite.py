import pygame


class Number(pygame.sprite.Sprite):     # Class For Numbers on the Resources

    def __init__(self, number, location):       # Initialises the Number Object
        pygame.sprite.Sprite.__init__(self)  # as super()
        self.image = pygame.image.load(f"../imgs/{number}.png").convert_alpha()
        self.rect = self.image.get_rect(center=location)
