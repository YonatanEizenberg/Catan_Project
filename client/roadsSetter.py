from Road import Road


class setRoads:  # Sets all the Roads of the game
    roads_dict = {}

    def __init__(self, points):  # a loop for all the Road to be Defined and entered to the dict
        for p1 in points:
            for p2 in points:
                if p1.check_points_close(p2):
                    road = Road(p1, p2)
                    if road.location not in self.roads_dict:
                        self.roads_dict[road.location] = road
                        p1.roads += [road]
                        p2.roads += [road]
        self.roads = list(self.roads_dict.values())

    def find_road(self, roadId, pointId):  # find a road by the given roadID and ensures by Point ID
        for road in list(self.roads_dict.values()):
            if str(road.id) == roadId:
                for pId in road.pointsId:
                    if str(pId) == pointId:
                        return road

    def find_close_available_roads(self, road):  # finds all the available and neighbouring roads to the given road
        roadsToBuild = []
        for r in list(self.roads_dict.values()):
            for pId in r.pointsId:
                if pId in road.pointsId and road != r and r.canBuild:
                    roadsToBuild += [r]
        return roadsToBuild
