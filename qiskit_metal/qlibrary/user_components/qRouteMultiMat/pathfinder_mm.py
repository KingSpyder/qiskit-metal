from qiskit_metal.qlibrary.tlines.pathfinder import RoutePathfinder
from .anchored_path_mm import RouteAnchors_mm

class RoutePathfinder_mm(RoutePathfinder, RouteAnchors_mm):
    pass