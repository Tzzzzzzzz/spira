import gdspy
import spira.all as spira
from spira.yevon.geometry.route.routes import Route


def RoutePath(port1, port2, path, width, layer):
    """  """
    start_straight=0
    end_straight=0
    pts = []

    p1 = port1.midpoint.to_numpy_array()
    p2 = port2.midpoint.to_numpy_array()

    if port1.orientation == 0:
        c1 = p1 + [start_straight, 0]
    if port2.orientation == 180:
        c2 = p2 - [start_straight, 0]

    pts.append(p1)
    if port1.orientation == 0:
        pts.append(c1)
    pts.extend(path)
    if port2.orientation == 180:
        pts.append(c2)
    pts.append(p2)

    path = gdspy.FlexPath(points=pts, width=1, corners='miter')
    R = Route(shape=path, p1=port1, p2=port2, layer=RDD.PLAYER.M6.METAL)
    return R

spira.RoutePath = RoutePath