import pygame


class Point(pygame.sprite.Sprite):

    def __init__(self, resource, location, id):    # Initialises Point in the Game
        pygame.sprite.Sprite.__init__(self)
        self.location = location
        self.canBuild = True
        self.resources = [resource]
        self.id = id
        self.relativeIds = {}           # Relative Ids are determined by their location on the different resources
        self.roads = []
        self.paths = {"circle": "../imgs/circle.png"}

        self.image = pygame.image.load("../imgs/circle.png").convert_alpha()
        self.rect = self.image.get_rect(center=location)

    def addResource(self, resource):                    # Adds Resource to the resources list
        self.resources += [resource]

    def build(self, sprites_group, points, settsBuilt, color):      # Builds a settlement on the Point
        self.setBuildFalse(sprites_group, points)
        self.paths["sett"] = f"../imgs/{color}set3.png"
        self.paths["city"] = f"../imgs/{color}city.png"
        self.image = pygame.image.load(self.paths["sett"]).convert_alpha()
        self.rect = self.image.get_rect(center=(self.location[0], self.location[1] - 3))
        sprites_group.add(self)
        settsBuilt += [self]

    def setBuildFalse(self, sprites_group, points):     # Setts the Build Option as False
        if self in sprites_group:
            sprites_group.remove(self)
        if self in points:
            points.remove(self)
        self.canBuild = False

    def check_points_close(self, p):                    # Checks if 2 Points are close to each other
        for relativeResId in self.relativeIds:          # by their Relative Ids
            for relativeResIdOther in p.relativeIds:
                if relativeResId == relativeResIdOther:
                    dif = (self.relativeIds[relativeResId] - p.relativeIds[relativeResIdOther]).__abs__()
                    if dif == 1 or dif == 5:
                        return True
        return False

    def show_image(self, string, sprites_group):        # Shows the image according to the string variable and the dict
        sprites_group.remove(self)
        self.image = pygame.image.load(self.paths[string]).convert_alpha()
        if string == "circle":
            self.rect = self.image.get_rect(center=self.location)
        else:
            self.rect = self.image.get_rect(center=(self.location[0], self.location[1] - 3))
        sprites_group.add(self)