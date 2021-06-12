class Road:     # The class for each road

    def __init__(self, location, id, pointsId):
        self.location = location
        self.canBuild = True
        self.id = id
        self.pointsId = pointsId

    def closeRoads(self, r):        # checks if the r road is close to self
        if self == r:
            return 0
        for pId in self.pointsId:
            if pId in r.pointsId:
                return int(pId)
        return 0


class setRoads:     # The class that sets all the roads
    roads = []

    def __init__(self, points):
        for p1 in points:
            for p2 in points:
                if p1.check_points_close(p2):
                    x1, y1 = p1.location
                    x2, y2 = p2.location
                    location = ((x1 + x2)/2, (y1 + y2)/2)
                    road = Road(location, (p1.pointId + p2.pointId)/2, [p1.pointId, p2.pointId])
                    p1.roads += [road]
                    p2.roads += [road]
                    self.roads += [road]



