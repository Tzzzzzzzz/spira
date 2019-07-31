import gdspy
import pyclipper
import numpy as np

from spira.core.parameters.variables import *

from copy import deepcopy
from spira.yevon.gdsii.base import __ShapeElement__
from spira.core.parameters.descriptor import FunctionParameter
from spira.yevon.geometry import shapes
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = [
    'Polygon',
    'Rectangle',
    'Box',
    'Circle',
    'Convex',
    'Cross',
    'Wedge',
    'Parabolic',
]


class Polygon(__ShapeElement__):
    """
    Element that connects shapes to the GDSII file format.
    Polygon are objects that represents the shapes in a layout.

    Examples
    --------
    >>> layer = spira.Layer(number=99)
    >>> rect_shape = spira.RectangleShape(p1=[0,0], p2=[1,1])
    >>> ply = spira.Polygon(shape=rect_shape, layer=layer)
    """

    _next_uid = 0

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.layer.process.symbol
        return self.__alias__

    def set_alias(self, value):
        if value is not None:
            self.__alias__ = value

    alias = FunctionParameter(get_alias, set_alias, doc='Functions to generate an alias for cell name.')

    def __init__(self, shape, layer, transformation=None, **kwargs):
        super().__init__(shape=shape, layer=layer, transformation=transformation, **kwargs)

        self.uid = Polygon._next_uid
        Polygon._next_uid += 1

    def __repr__(self):
        if self is None:
            return 'Polygon is None!'
        layer = RDD.GDSII.IMPORT_LAYER_MAP[self.layer]
        class_string = "[SPiRA: Polygon \'{}\'] (center {}, vertices {}, process {}, purpose {})"
        return class_string.format(self.alias, self.center, self.count, self.layer.process.symbol, self.layer.purpose.symbol)

    def __str__(self):
        return self.__repr__()

    def __hash__(self):
        return hash(self.__repr__())

    # NOTE: We are not copying the ports, so they
    # can be re-calculated for the transformed shape.
    def __deepcopy__(self, memo):
        # ports = self.ports.transform_copy(self.transformation)
        # return self.__class__(
        return Polygon(
            shape=deepcopy(self.shape),
            layer=deepcopy(self.layer),
            ports=deepcopy(self.ports),
            # ports=self.ports.transform_copy(self.transformation),
            transformation=deepcopy(self.transformation)
        )

    def short_string(self):
        return "Polygon [{}, {}, {}]".format(self.center, self.layer.process.symbol, self.layer.purpose.symbol)

    def flat_copy(self, level=-1):
        """ Flatten a copy of the polygon. """
        S = Polygon(shape=self.shape, layer=self.layer, transformation=self.transformation)
        S.expand_transform()
        return S

    def nets(self, lcar):
        from spira.yevon.geometry.nets.net import Net
        from spira.yevon.vmodel.geometry import GmshGeometry
        from spira.yevon import filters

        if self.layer.purpose.symbol == 'METAL':

            if RDD.ENGINE.GEOMETRY == 'GMSH_ENGINE':
                geometry = GmshGeometry(lcar=lcar,
                    process=self.layer.process,
                    process_polygons=[deepcopy(self)])

            cc = []
            for p in self.ports:
                p = p.transform(self.transformation)
                if p.purpose == RDD.PURPOSE.PORT.PIN:
                    cc.append(p)
                elif p.purpose == RDD.PURPOSE.PORT.CONTACT:
                    cc.append(p)

            F = filters.ToggledCompositeFilter()
            F += filters.NetProcessLabelFilter(process_polygons=[deepcopy(self)])
            F += filters.NetDeviceLabelFilter(device_ports=cc)
            F += filters.NetEdgeFilter(process_polygons=deepcopy(self))

            net = Net(name=self.layer.process.symbol, geometry=geometry)

            net = F(net)[0]

            # from spira.yevon.utils.netlist import combine_net_nodes
            # net = combine_net_nodes(net=net, algorithm=['d2d'])

            # from spira.yevon.geometry.nets.net import CellNet
            # cn = CellNet()
            # cn.g = net.g
            # cn.generate_branches()
            # cn.detect_dummy_nodes()

            # return cn

            return net

        return []


def Rectangle(layer, p1=(0,0), p2=(2,2), center=(0,0), alias=None, transformation=None):
    """ Creates a rectangular shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Rectangle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.RectangleShape(p1=p1, p2=p2)
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Box(layer, width=1, height=1, center=(0,0), alias=None, transformation=None):
    """ Creates a box shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Box(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.BoxShape(width=width, height=height, center=center)
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Circle(layer, box_size=(1,1), angle_step=1, center=(0,0), alias=None, transformation=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CircleShape(box_size=box_size, angle_step=angle_step)
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Convex(layer, radius=1.0, num_sides=6, center=(0,0), alias=None, transformation=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ConvexShape(radius=radius, num_sides=num_sides)
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Cross(layer, box_size=20, thickness=5, center=(0,0), alias=None, transformation=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.CrossShape(box_size=box_size, thickness=thickness)
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Wedge(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3,
          end_width=1, center=(0,0), alias=None, transformation=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.WedgeShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)


def Parabolic(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3,
              end_width=1, center=(0,0), alias=None, transformation=None):
    """ Creates a circle shape that can be used in 
    GDSII format as a polygon object.

    Example
    -------
    >>> p = spira.Circle(p1=(0,0), p2=(10,0), layer=RDD.PLAYER.M6)
    >>> [SPiRA: Rectangle] ()
    """
    shape = shapes.ParabolicShape(
        begin_coord=begin_coord, 
        end_coord=end_coord, 
        begin_width=begin_width, 
        end_width=end_width
    )
    return Polygon(alias=alias, shape=shape, layer=layer, transformation=transformation)

