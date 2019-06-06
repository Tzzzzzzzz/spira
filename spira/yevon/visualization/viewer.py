import spira.all as spira
from spira.yevon.geometry import shapes
from spira.yevon.geometry.ports.port import ContactPort
from spira.core.parameters.descriptor import DataField
from spira.yevon.process.physical_layer import PhysicalLayer
from spira.yevon.process import get_rule_deck
from spira.yevon.geometry.vector import transformation_from_vector


RDD = get_rule_deck()


__all__ = ['PortLayout']


class PortLayout(spira.Cell):
    """  """

    port = spira.PortField()

    edge = DataField(fdef_name='create_edge')
    arrow = DataField(fdef_name='create_arrow')
    label = DataField(fdef_name='create_label')

    def create_edge(self):
        dw = self.port.width
        dl = self.port.length
        layer = PhysicalLayer(process=self.port.process, purpose=self.port.purpose)
        p = spira.Box(width=dw, height=dl, layer=layer)
        T = transformation_from_vector(self.port) + spira.Rotation(-90)
        # T += self.transformation
        p.transform(T)
        return p

    def create_arrow(self):
        layer = PhysicalLayer(self.port.process, RDD.PURPOSE.PORT.DIRECTION)
        # w = self.port.length * 3
        w = 0.05*1e6
        # l = 2*1e6
        l = self.port.length * 5
        arrow_shape = shapes.ArrowShape(width=w, length=l, head=l*0.2)
        p = spira.Polygon(shape=arrow_shape, layer=layer, enable_edges=False)
        T = transformation_from_vector(self.port)
        p.transform(T)
        return p

    def create_label(self):
        layer = PhysicalLayer(self.port.process, RDD.PURPOSE.PORT.DIRECTION)
        return spira.Label(
            position=self.port.midpoint,
            text=self.port.name,
            orientation=self.port.orientation,
            layer=layer
        )

    def create_elementals(self, elems):
        elems += self.edge
        elems += self.label
        if not isinstance(self.port, ContactPort):
            elems += self.arrow
        return elems

