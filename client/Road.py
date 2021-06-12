import pygame


class Road(pygame.sprite.Sprite):           # class for the Roads of the game

    def __init__(self, p1, p2):             # initialises the Road Object
        pygame.sprite.Sprite.__init__(self)
        x1, y1 = p1.location
        x2, y2 = p2.location
        location = ((x1 + x2) / 2, (y1 + y2) / 2)
        self.location = location
        self.id = (p1.id + p2.id) / 2
        self.pointsId = [p1.id, p2.id]
        self.canBuild = True
        if x1 == x2:
            self.slope = 4                 # the slope will be used to choose the image of the road, there are 3 images
        else:
            s = (y1 - y2) / (x1 - x2)
            if s > 0:
                self.slope = 2
            else:
                self.slope = 3
        self.image = pygame.image.load("../imgs/circle.png").convert_alpha()    # In the beginning, there is an image
        self.rect = self.image.get_rect(center=location)                        # of a circle instead of the Road

    def build(self, sprites_group, roadsToBuild, color):    # Builds a Road on the Road's Object for the Player
        roadsToBuild.remove(self)
        self.canBuild = False
        print("changed image of road")
        self.image = pygame.image.load(f"../imgs/{color}road{self.slope}.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.location)
        sprites_group.add(self)

    def build_opp(self, sprites_group, color):              # Builds a Road on the Road's Object for an Opponent
        self.image = pygame.image.load(f"../imgs/{color}road{self.slope}.png").convert_alpha()
        self.rect = self.image.get_rect(center=self.location)
        sprites_group.add(self)
        self.canBuild = False

    def find_close_available_points(self, points):          # the function is receiving a list of all points
        settsToBuild = []                                   # and returns a list of the neighbouring points
        for point in points:                                # to the Road by their POINT ID that you can build on
            if point.id in self.pointsId and point.canBuild and point not in settsToBuild:
                settsToBuild += [point]
        return settsToBuild