from Resource import Resource


class setResources:  # Sets all the Resources of the game
    locations = []
    row = [(3, (349.5, 98)), (4, (320, 149)), (5, (290.5, 200)), (4, (320, 251)), (3, (349.5, 302))]
    resources = []  # list of all the Resources

    def __init__(self, msg_list, sprites_group, resources):
        line_counter = 1
        id = 0
        column_counter = 0
        max_counter, location = self.row[column_counter]
        for part in msg_list:   # a loop for all the points to be Defined and entered to the dict
            if part:
                char = part[0]
                number = part[1::]
                r = Resource(char, number, location, id)    # Initialises a Resource
                id += 1
                resources += [r]
                self.resources += [r]
                sprites_group.add(r)
                if int(r.number) > 0:
                    sprites_group.add(r.number_sprite)
                line_counter += 1
                location = (location[0] + r.rect.width, location[1])
                if line_counter - 1 == max_counter:
                    line_counter = 1
                    column_counter += 1
                    if len(self.row) == column_counter:
                        return
                    max_counter, location = self.row[column_counter]