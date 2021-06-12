from Point import Point


class setPoints:  # Sets all the Points of the game
    everyRes = [(29.5, 5), (0, 22), (0, 56), (29.5, 73), (59, 56), (59, 22)]  # all locations of Points from resource
    pointsDict = {}  # Dictionary of all the points, keys = points' location, values = the points

    def __init__(self, resources):  # a loop for all the points to be Defined and entered to the dict
        id = 0
        for resource in resources:
            for i in range(6):
                pLocation = (resource.location[0] + setPoints.everyRes[i][0],
                             resource.location[1] + setPoints.everyRes[i][1])
                if pLocation in self.pointsDict:  # if the location is in the dict, than the point exists
                    self.pointsDict[pLocation].addResource(resource)  # and you need to add the resource
                else:  # else we need to define the Point
                    p = Point(resource, pLocation, id)
                    self.pointsDict[pLocation] = p
                    id += 1
                self.pointsDict[pLocation].relativeIds[resource.id] = i

    def returnValues(self):  # Returns a List of all the Points in the game
        return list(self.pointsDict.values())

    def find_point(self, id):  # Returns a Point by the given POINT ID
        for point in self.pointsDict.values():
            if point.id == int(id):
                return point
        return None
