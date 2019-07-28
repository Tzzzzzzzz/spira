import gdspy
import pyclipper
import numpy as np

from copy import deepcopy
from spira.core.transforms import stretching
from spira.yevon.geometry import bbox_info
from spira.yevon.utils import clipping
from spira.yevon.gdsii.base import __LayerElement__
from spira.yevon.geometry.coord import CoordParameter, Coord
from spira.core.parameters.descriptor import ParameterDescriptor, FunctionParameter, Parameter
from spira.yevon.geometry.ports.base import __Port__
from spira.core.parameters.variables import *
from spira.core.transforms.stretching import *
from spira.yevon.geometry import shapes
from spira.yevon.geometry.shapes import ShapeParameter
from spira.yevon.process.gdsii_layer import Layer
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


class __ShapeElement__(__LayerElement__):
    """ Base class for an edge element. """

    shape = ShapeParameter()

    @property
    def points(self):
        return self.shape.points

    @property
    def area(self):
        return gdspy.Polygon(self.shape.points).area()

    @property
    def count(self):
        return np.size(self.shape.points, 0)

    @property
    def center(self):
        return self.bbox_info.center

    @center.setter
    def center(self, destination):
        self.move(midpoint=self.center, destination=destination)

    @property
    def bbox_info(self):
        return self.shape.bbox_info.transform_copy(self.transformation)

    def id_string(self):
        return '{} - hash {}'.format(self.short_string(), self.shape.hash_string)

    def is_empty(self):
        """ Returns `False` is the polygon shape has no points. """
        return self.shape.is_empty()

    def encloses(self, point):
        """ Returns `True` if the polygon encloses the point. """
        from spira.yevon.utils import clipping
        shape = self.shape.transform_copy(self.transformation)
        return clipping.encloses(coord=point, points=shape.points)

    def expand_transform(self):
        """ Expand the transform by applying it to the shape. """
        from spira.core.transforms.identity import IdentityTransform
        if not self.transformation.is_identity():
            self.shape = self.shape.transform_copy(self.transformation)
            self.transformation = IdentityTransform()
        return self

    def flatten(self, level=-1):
        """ Flatten the polygon without creating a copy. """
        return self.expand_transform()

    # # FIXME: Move this to an output generator.
    # def convert_to_gdspy(self, transformation=None):
    #     """ Converts a SPiRA polygon to a Gdspy polygon.
    #     The extra transformation parameter is the
    #     polygon edge ports. """
    #     layer = RDD.GDSII.EXPORT_LAYER_MAP[self.layer]
    #     T = self.transformation + transformation
    #     shape = self.shape.transform_copy(T)
    #     return gdspy.Polygon(points=shape.points, layer=layer.number, datatype=layer.datatype)

    def fillet(self, radius, angle_resolution=128, precision=0.001):
        """ Applies fillet rounding algorithm to polygon corners. """
        super().fillet(radius=radius, points_per_2pi=angle_resolution, precision=precision)
        self.shape.points = self.polygons
        return self

    def stretch(self, factor=(1,1), center=(0,0)):
        """ Stretches the polygon by a factor. """
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply(self)

    def stretch_copy(self, factor=(1,1), center=(0,0)):
        """ Stretches a copy of the polygon by a factor. """
        T = spira.Stretch(stretch_factor=factor, stretch_center=center)
        return T.apply_copy(self)

    def stretch_port(self, port, destination):
        """ The element by moving the subject port, without 
        distorting the entire element. Note: The opposite 
        port position is used as the stretching center. """
        opposite_port = bbox_info.bbox_info_opposite_boundary_port(self, port)
        T = stretching.stretch_element_by_port(self, opposite_port, port, destination)
        T.apply(self)
        return self

    def move(self, midpoint=(0,0), destination=None, axis=None):
        """ Moves the polygon from `midpoint` to a `destination`. """

        if destination is None:
            destination = midpoint
            midpoint = Coord(0,0)

        if isinstance(midpoint, Coord):
            m = midpoint
        elif np.array(midpoint).size == 2:
            m = Coord(midpoint)
        elif issubclass(type(midpoint), __Port__):
            m = midpoint.midpoint
        else:
            raise ValueError('Midpoint error')

        if issubclass(type(destination), __Port__):
            d = destination.midpoint
        if isinstance(destination, Coord):
            d = destination
        elif np.array(destination).size == 2:
            d = Coord(destination)
        else:
            raise ValueError('Destination error')

        dxdy = d - m
        self.translate(dxdy)
        return self


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

    edges = Parameter(fdef_name='create_edges')

    def get_alias(self):
        if not hasattr(self, '__alias__'):
            self.__alias__ = self.process
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
        return class_string.format(self.alias, self.center, self.count, self.process, self.purpose)

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
        return "Polygon [{}, {}, {}]".format(self.center, self.process, self.purpose)

    def create_edges(self):
        """ Generate default edges for this polygon.
        These edges can be transformed using adapters. """
        from spira.yevon.geometry.edges.edges import generate_edges
        return generate_edges(
            shape=self.shape, layer=self.layer,
            internal_pid=self.id_string(),
            transformation=self.transformation
        )

    def flat_copy(self, level=-1):
        """ Flatten a copy of the polygon. """
        S = Polygon(shape=self.shape, layer=self.layer, transformation=self.transformation)
        S.expand_transform()
        return S

    def nets(self, lcar):
        from spira.yevon.geometry.nets.net import Net
        from spira.yevon.vmodel.geometry import GmshGeometry
        from spira.yevon import filters

        if self.purpose == 'METAL':

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

            F = filters.ToggledCompoundFilter()
            F += filters.NetProcessLabelFilter(process_polygons=[deepcopy(self)])
            F += filters.NetDeviceLabelFilter(device_ports=cc)
            F += filters.NetEdgeFilter(process_polygons=deepcopy(self))

            net = Net(name=self.process, geometry=geometry)

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


def Wedge(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3, end_width=1,
          center=(0,0), alias=None, transformation=None):
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


def Parabolic(layer, begin_coord=(0,0), end_coord=(10,0), begin_width=3, end_width=1,
              center=(0,0), alias=None, transformation=None):
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

