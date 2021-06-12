class Point:       # The class for each Point
    id = 0

    def __init__(self, resource, location, relativeId):     # Initialises the Point
        self.location = location
        self.resources = [resource]
        self.pointId = Point.id
        Point.id += 1
        self.vacant = True
        self.relativeIds = {}
        self.relativeIds[resource.resId] = relativeId
        self.roads = []

    def addResource(self, resource, relativeId):        # adds resource to the self.resources list
        self.resources += [resource]
        self.relativeIds[resource.resId] = relativeId

    def check_points_close(self, p):        # checks if the self point and p are close to each other by the relative ID
        for relativeResId in self.relativeIds:
            for relativeResIdOther in p.relativeIds:
                if relativeResId == relativeResIdOther:
                    dif = (self.relativeIds[relativeResId] - p.relativeIds[relativeResIdOther]).__abs__()
                    if dif == 1 or dif == 5:
                        return True
        return False

    def initial_earning(self):      # calculates the initial earnings of the point
        earnings = {}
        for resource in self.resources:
            if resource.char != "d":
                if not earnings.__contains__(resource.char):
                    earnings[resource.char] = 1
                else:
                    earnings[resource.char] += 1
        return earnings


class setPoints:        # Class that sets all the points
    everyRes = [(29.5, 5), (0, 22), (0, 56), (29.5, 73), (59, 56), (59, 22)]
    pointsArray = {}

    def __init__(self, resources):
        for resource in resources:
            counter = 0
            for i in range(6):
                pLocation = (resource.location[0] + self.everyRes[i][0],
                             resource.location[1] + self.everyRes[i][1])
                if pLocation in self.pointsArray:
                    self.pointsArray[pLocation].addResource(resource, i)
                else:
                    p = Point(resource, pLocation, i)
                    self.pointsArray[pLocation] = p
                    counter += 1
            print(counter)

    def find_point(self, id):       # finds point by the point ID
        for point in self.pointsArray.values():
            if point.pointId == int(id):
                return point
        return None

    def buildStatus(self, point, playerId):     # returns the response for build with all the close points
        points_for_response = []
        for p in self.pointsArray.values():
            if point.check_points_close(p):
                points_for_response += [p]
        response = f"build_sett:{playerId}:{point.pointId}:"
        pointsId = [str(p.pointId) for p in points_for_response]
        res = ",".join(pointsId)
        return response + res
