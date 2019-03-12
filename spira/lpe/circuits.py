import spira
import time
import numpy as np
from spira import param, shapes
from spira.lpe import mask
from spira import pc
from spira.lpe.containers import __CellContainer__, __NetContainer__, __CircuitContainer__
from spira.lne.net import Net
from copy import copy, deepcopy
from spira.lpe.devices import Device
from spira.lpe.structure import Structure

from spira.lgm.route.routing import Route
from spira.lgm.route.route_shaper import RouteSimple, RouteGeneral
from spira.core.mixin.netlist import NetlistSimplifier
from spira.lpe.structure import __NetlistCell__
from spira.lpe.boxes import BoundingBox
from halo import Halo
from spira.utils import boolean


RDD = spira.get_rule_deck()


class RouteToStructureConnector(__CircuitContainer__, Structure):
    """  """

    def create_contacts(self, boxes):
        start = time.time()
        print('[*] Connecting routes with devices')
        self.unlock_ports()
        for D in self.structures:
            if isinstance(D, spira.SRef):
                B = BoundingBox(S=D)
                boxes += B
        end = time.time()
        print('Block calculation time {}:'.format(end - start))
        return boxes

    def unlock_ports(self):
        for R in self.routes:
            for D in self.structures:
                # self.__unlock_route_edges__(R, D)
                self.__unlock_device_edges__(R, D)

    def __unlock_route_edges__(self, R, D):
        for M in D.ref.metals:
            M_ply = M.polygon
            M_ply.transform(D.tf)
            for key, port in R.instance_ports.items():
                for mp in M_ply.shape.points:
                    if port.encloses(mp):
                        R.port_locks[port.key] = False

    def __unlock_device_edges__(self, R, D):
        for pp in R.ref.metals:
            if isinstance(pp, pc.ProcessLayer):
                R_ply = pp.polygon
                for key, port in D.instance_ports.items():
                    if isinstance(port, (spira.Term, spira.EdgeTerm)):
                        if port.gdslayer.number == pp.player.layer.number:
                            if R_ply & port.edge:
                                route_key = (pp.node_id, pp.player.layer.number)
                                D.port_connects[key] = route_key
                                D.port_locks[key] = False


class Circuit(RouteToStructureConnector):
    """ Deconstructs the different hierarchies in the cell. """

    __mixins__ = [NetlistSimplifier]

    algorithm = param.IntegerField(default=6)
    level = param.IntegerField(default=2)
    lcar = param.IntegerField(default=10)

    def create_elementals(self, elems):
        # for e in self.structures:
        #     elems += e
        # for e in self.routes:
        #     elems += e
        for e in self.merged_layers:
            elems += e
        return elems

    def create_primitives(self, elems):
        elems = deepcopy(self.ports)
        for p in self.terminals:
            elems += p
        return elems

    def create_structures(self, structs):
        if self.cell is not None:
            for S in self.cell.elementals:
                if isinstance(S, spira.SRef):
                    structs += S
        else:
            for e in self.elementals.sref:
                if issubclass(type(e), (Device, Circuit)):
                    structs += e
        return structs

    def create_routes(self, routes):
        if self.cell is not None:
            r = Route(cell=self.cell)
            routes += spira.SRef(r)
        else:
            for e in self.elementals.sref:
                if issubclass(type(e), Route):
                    routes += e
        return routes

    def create_metals(self, elems):
        R = self.routes.flat_copy()
        B = self.contacts.flat_copy()
        for player in RDD.PLAYER.get_physical_layers(purposes='METAL'):
            Rm = R.get_polygons(layer=player.layer)
            Bm = B.get_polygons(layer=player.layer)
            for i, e in enumerate([*Rm, *Bm]):
                # alias = 'ply_{}_{}_{}'.format(player.layer.number, self.cell.node_id, i)
                alias = 'ply_{}_{}_{}'.format(player.layer.number, self.__class__.__name__, i)
                # alias = 'ply_{}_{}_{}'.format(player.layer.number, 'webfwejfbjk', i)
                elems += pc.Polygon(name=alias, player=player, points=e.polygons, level=self.level)
        return elems

    def create_ports(self, ports):
    # def create_connector_ports(self, ports):

        print('\n[*] Calculate Layout ports')

        start = time.time()

        self.unlock_ports()

        for D in self.structures:
            for name, port in D.instance_ports.items():
                if port.locked is False:
                    edgelayer = deepcopy(port.gdslayer)
                    edgelayer.datatype = 100
                    ports += port.modified_copy(edgelayer=edgelayer)

        for R in self.routes:
            for name, port in R.instance_ports.items():
                if port.locked is False:
                    edgelayer = deepcopy(port.gdslayer)
                    edgelayer.datatype = 101
                    ports += port.modified_copy(edgelayer=edgelayer)

        # -------------------------------------------------------------------

        # for p in self.terminals:
        #     ports += p

        # for pl in RDD.PLAYER.get_physical_layers(purposes='METAL'):
        #     for m in self.get_metals(pl):
        #         for p in m.ports:
        #             for t in self.terminals:
        #                 edgelayer = deepcopy(p.gdslayer)
        #                 edgelayer.datatype = 82
        #                 arrowlayer = deepcopy(p.gdslayer)
        #                 arrowlayer.datatype = 83
        #                 if p.encloses_midpoint(points=t.edge.polygons):
        #                     ports += spira.Term(
        #                         name=t.name,
        #                         midpoint=p.midpoint,
        #                         orientation=p.orientation,
        #                         edgelayer=edgelayer,
        #                         arrowlayer=arrowlayer,
        #                         width=p.width,
        #                     )

        end = time.time()
        print('Layout port calculation time {}:'.format(end - start))

        return ports

    def create_terminals(self, ports):

        # FIXME!!! Needed for terminal detection in the Mesh.
        if self.cell is not None:
            cell = deepcopy(self.cell)
            flat_elems = cell.flat_copy()
            port_elems = flat_elems.get_polygons(layer=RDD.PURPOSE.TERM)
            label_elems = flat_elems.labels
            for port in port_elems:
                for label in label_elems:
                    lbls = label.text.split(' ')
                    s_p1, s_p2 = lbls[1], lbls[2]
                    p1, p2 = None, None
                    for m1 in RDD.PLAYER.get_physical_layers(purposes=['METAL', 'GND']):
                        if m1.layer.name == s_p1:
                            p1 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                        if m1.layer.name == s_p2:
                            p2 = spira.Layer(name=lbls[0],
                                number=m1.layer.number,
                                datatype=RDD.GDSII.TEXT
                            )
                    if p1 and p2 :
                        for pts in port.polygons:
                            # if label.encloses(ply=port.polygons[0]):
                            if label.encloses(ply=pts):
                                ports += spira.Term(
                                    name=label.text,
                                    layer1=p1, layer2=p2,
                                    width=port.dx,
                                    midpoint=label.position
                                )

        return ports

    def create_netlist(self):
        self.g = self.merge

        # Algorithm 1
        self.g = self.nodes_combine(algorithm='d2d')
        # Algorithm 2
        self.g = self.generate_branches()
        # Algorithm 3
        self.detect_dummy_nodes()
        # Algorithm 4
        self.g = self.generate_branches()
        # Algorithm 5
        self.g = self.nodes_combine(algorithm='b2b')

        self.plot_netlist(G=self.g, graphname=self.name, labeltext='id')

        return self.g


