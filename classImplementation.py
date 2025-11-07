#sudo apt install ros-noetic-lanelet2 or pip install lanelet2 if you dont have ros
import lanelet2
from lanelet2.core import BasicPoint2d, Lanelet
from lanelet2 import io, geometry, traffic_rules, projection, routing, maps 
from lanelet2.projection import UtmProjector, Origin 


class RouteRequestHandler:
    pass
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
    pass
class PathFinder:
    pass

if __name__ == "__main__":
    #initialize loader
    loader = MapLoader("enlaneletmapfinal.osm")
    laneletMapData = loader.loadMap()

    mapObj = LaneletMap(laneletMapData)

    #test 
    mapObj.print_summary()
    nearest = mapObj.getNearestLanelet(37.123, -122.456)
    if nearest:
        print(f"nearest ll id: {nearest.id}")
