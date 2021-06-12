class Resource:  # The class for each road
    id = 0

    def __init__(self, char, number, location):
        self.char = char
        self.number = number
        self.location = location
        self.resId = Resource.id
        Resource.id += 1


class set_resources:  # The class that sets all the roads
    locations = [(349.5, 98), (408.5, 98), (467.5, 98), (320, 149), (379, 149), (438, 149), (497, 149), (290.5, 200)
        , (349.5, 200), (408.5, 200), (467.5, 200), (526.5, 200), (320, 251),
                 (379, 251), (438, 251), (497, 251), (349.5, 302), (408.5, 302), (467.5, 302)]
    resources = []

    def __init__(self, board_order):
        id = 0
        for charNum in board_order:
            char = charNum[0]
            num = charNum[1::]
            r = Resource(char, num, self.locations[id])
            self.resources += [r]
            id += 1
