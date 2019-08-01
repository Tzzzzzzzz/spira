from spira.yevon.gdsii.cell import Cell
from spira.yevon.utils import netlist
from spira.yevon.gdsii.elem_list import ElementListParameter, ElementList
from spira.yevon.geometry.ports import PortList
from copy import deepcopy

from spira.core.parameters.variables import *
from spira.yevon.process import get_rule_deck


RDD = get_rule_deck()


__all__ = ['PCell', 'Device', 'Circuit']


class PCell(Cell):
    """  """

    pcell = BoolParameter(default=True)
    routes = ElementListParameter(doc='List of `Route` elements connected to the cell.')
    structures = ElementListParameter(doc='List of cell structures that coalesces the top-level cell.')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)


class Device(PCell):
    """  """

    # lcar = NumberParameter(default=RDD.PCELLS.LCAR_DEVICE)
    lcar = NumberParameter(default=1)

    def __init__(self, pcell=True, **kwargs):
        super().__init__(**kwargs)
        self.pcell = pcell

    def __repr__(self):
        class_string = "[SPiRA: Device(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        if self.pcell is True:

            D = Cell(elements=elems.flat_copy())

            F = RDD.PCELLS.FILTERS
            F['boolean'] = True
            F['simplify'] = True
            # F['via_contact'] = True
            F['via_contact'] = False
            F['metal_connect'] = False

            elems = F(D).elements

            # D = Cell(elements=elems)
            # elems = D.elements

        return elems

    def create_netlist(self):

        print('Device netlist')

        net = super().create_netlist()
        net = netlist.combine_net_nodes(net=net, algorithm=['d2d'])
        net = netlist.combine_net_nodes(net=net, algorithm=['s2s'])
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])

        # import networkx as nx
        # from spira.yevon.geometry.nets.net import Net
        # net = self.nets(lcar=self.lcar).disjoint(connect=True)
        # graphs = list(nx.connected_component_subgraphs(net.g))
        # net = Net(g=nx.disjoint_union_all(graphs))

        return net


class Circuit(PCell):
    """  """

    corners = StringParameter(default='miter', doc='Define the type of path joins.')
    bend_radius = NumberParameter(allow_none=True, default=None, doc='Bend radius of path joins.')

    lcar = NumberParameter(default=RDD.PCELLS.LCAR_CIRCUIT)

    def __repr__(self):
        class_string = "[SPiRA: Circuit(\'{}\')] (elements {}, ports {})"
        return class_string.format(self.name, self.elements.__len__(), self.ports.__len__())

    def __str__(self):
        return self.__repr__()

    def __create_elements__(self, elems):
        from spira.yevon.gdsii.sref import SRef

        # print('\n[*] Circuit elements\n')

        elems = self.create_elements(elems)
        elems += self.structures
        elems += self.routes

        def wrap_references(cell, c2dmap, devices):
            for e in cell.elements.sref:
                if isinstance(e.reference, Device):
                    D = deepcopy(e.reference)
                    D.elements.transform(e.transformation)
                    D.ports.transform(e.transformation)
                    devices[D] = D.elements
                    D.elements = ElementList()
                    S = deepcopy(e)
                    S.reference = D
                    c2dmap[cell] += S
                else:
                    S = deepcopy(e)
                    S.reference = c2dmap[e.reference]
                    c2dmap[cell] += S

        if self.pcell is True:

            c2dmap = {}
            ex_elems = elems.expand_transform()

            C = Cell(elements=ex_elems)

            devices = {}

            for cell in C.dependencies():
                D = Cell(name=cell.name, elements=deepcopy(cell.elements.polygons))
                c2dmap.update({cell:D})

            for cell in C.dependencies():
                wrap_references(cell, c2dmap, devices)

            D = c2dmap[C]

            F = RDD.PCELLS.FILTERS
            F['boolean'] = True
            F['simplify'] = True
            F['via_contact'] = False
            F['metal_connect'] = False

            Df = F(D)

            for d in Df.dependencies():
                if d in devices.keys():
                    d.elements = devices[d]

            elems = Df.elements

        return elems

    def create_netlist(self):

        print('Circuit netlist')

        net = super().create_netlist()
        net = netlist.combine_net_nodes(net=net, algorithm=['d2d'])
        # net = netlist.combine_net_nodes(net=net, algorithm=['s2s'])
        # net = netlist.combine_net_nodes(net=net, algorithm=['d2d', 's2s'])

        return net



