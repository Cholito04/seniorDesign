#sudo apt install ros-noetic-lanelet2 or pip install lanelet2 if you dont have ros
import lanelet2
from lanelet2.core import BasicPoint2d
from lanelet2 import io, geometry, traffic_rules, projection, routing
from lanelet2.projection import UtmProjector, Origin
import csv


class RouteRequestHandler:
    def __init__(self, startLocation=None, goalLocation=None):
        self.startLocation = startLocation
        self.goalLocation = goalLocation
    def getUsersInput(self):
        start_lat = float(input("Enter start latitude: "))
        start_lon = float(input("Enter start longitude: "))
        goal_lat = float(input("Enter goal latitude: "))
        goal_lon = float(input("Enter goal longitude: "))
        self.startLocation = (start_lat, start_lon)
        self.goalLocation = (goal_lat, goal_lon)
    def validateInput(self, laneletMap):
        start_ll = laneletMap.getNearestLanelet(*self.startLocation)
        goal_ll = laneletMap.getNearestLanelet(*self.goalLocation)
        if not start_ll or not goal_ll:
            print("Error with coordinates")
            return None, None
        print(f"Start={start_ll.id}, Goal={goal_ll.id}")
        return start_ll, goal_ll

class MapLoader:
    def __init__(self, mapFile: str):
        self.mapFile = mapFile
        self.projector = None
        self.map = None
    def loadMap(self): 
        #load and parse the lanelet2 map from an osm file
        origin = Origin(0.0, 0.0)  #set origin point later
        self.projector = UtmProjector(origin)
        self.map = io.load(self.mapFile, self.projector)
        print(f"loaded map with {len(self.map.laneletLayer)} lanelets") #tells you the # of lanelets in map
        return self.map   
class LaneletMap:
    def __init__(self, laneMap):
        self.map = laneMap

    def getNearestLanelet(self, lat, lon):
        #find nearest lanelet for routing purposes
        point = BasicPoint2d(lat , lon)
        nearest = geometry.nearestLanelet(self.map, point)
        return nearest
    
    def getLaneletIds(self):
        #return IDs of all lanelets in the map to test if map is loaded properly
        return [ll.id for ll in self.map.laneletLayer]

    def printSummary(self):
        print(f"Map contains {len(self.map.laneletLayer)} lanelets")
    
class RoutePlanner:
    def __init__(self, laneletMap):
        self.laneletMap = laneletMap
        self.rules = traffic_rules.create(
            traffic_rules.Locations.Germany, 
            traffic_rules.Participants.Vehicle
        )
        self.graph = routing.RoutingGraph(self.laneletMap.map, self.rules)
    def computeRoutes(self, start_ll, goal_ll):
        route = self.graph.getRoute(start_ll, goal_ll)
        if route:
            print(f"Route from {start_ll.id} to {goal_ll.id}.")
        else:
            print("No route found")
        return route
class PathFinder:
    def __init__(self, route):
        self.route = route
        self.path = []
    def generatePath(self, route=None):
        if route:
            self.route = route
        shortest_path = self.route.shortestPath()
        if not shortest_path:
            print("No paths")
            return []
        coords = []
        for ll in shortest_path:
            centerline = ll.centerline
            for pt in centerline:
                coords.append((pt.x, pt.y))
        self.path = coords
        print(f"Generated path with {len(coords)} points")
        return coords

if __name__ == "__main__":
     #initialize loader
    loader = MapLoader("enlaneletmapfinal.osm")
    laneletMapData = loader.loadMap()
    mapObj = LaneletMap(laneletMapData)
    mapObj.printSummary()

    handler = RouteRequestHandler()
    handler.getUsersInput()

    start_ll, goal_ll = handler.validateInput(mapObj)
    if start_ll and goal_ll:
        planner = RoutePlanner(mapObj)
        route = planner.computeRoutes(start_ll, goal_ll)
        if route:
            finder = PathFinder(route)
            finder.generatePath()
            finder.exportPath("path.csv")