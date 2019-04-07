import spira
import numpy as np
from copy import deepcopy
from spira.core import param
from spira import shapes
from spira.visualization import color
from spira.process.processlayer import ProcessLayer


class Polygon(ProcessLayer):

    color = param.ColorField(default=color.COLOR_BLUE_VIOLET)
    points = param.ElementalListField()
    
    def __deepcopy__(self, memo):
        return Polygon(
            points=self.points,
            elementals=deepcopy(self.elementals),
            ps_layer=self.ps_layer,
            # polygon=deepcopy(self.polygon),
            node_id=deepcopy(self.node_id),
        )

    def create_elementals(self, elems):
        ply = spira.Polygons(shape=self.points, gds_layer=self.layer)
        if self.transformation is not None:
            print(ply)
            ply.transform_copy(self.transformation)
            print(ply)
        elems += ply
        return elems






