import spira 
import networkx as nx
from spira import param, shapes
from spira.gdsii.elemental.port import __Port__


class __NetlistSimplifier__(object):

    _ID = 0

    __stored_paths__ = []

    def __remove_nodes__(self):
        remove = list()
        text = self.__get_called_id__()
        for n in self.g.nodes():
            # if 'device' in self.g.node[n]:
            #     # e = tuple([i for i in self.g[n]])
            #     # self.g.add_edge(*e, label=None)
            #     if not issubclass(type(self.g.node[n]['device']), __Port__):
            #         remove.append(n)
            if 'device' not in self.g.node[n]:
                # if 'path' not in self.g.node[n]:
                remove.append(n)
            elif isinstance(self.g.node[n]['device'], spira.Label):
                if self.g.node[n]['device'].text != text:
                    remove.append(n)

        self.g.remove_nodes_from(remove)

    def __validate_path__(self, path):
        """ Test if path contains masternodes. """
        valid = True
        s, t = path[0], path[-1]
        if self.__is_path_stored__(s, t):
            valid = False
        if s not in self.branch_nodes:
            valid = False
        if t not in self.branch_nodes:
            valid = False
        for n in path[1:-1]:
            if 'device' in self.g.node[n]:
                D = self.g.node[n]['device']
                if issubclass(type(D), (__Port__, spira.SRef)):
                    valid = False
        return valid

    def __store_branch_paths__(self, s, t):
        if nx.has_path(self.g, s, t):
            for p in nx.all_simple_paths(self.g, source=s, target=t):
                if self.__validate_path__(p):
                    self.__stored_paths__.append(p)

    def __is_path_stored__(self, s, t):
        for path in self.__stored_paths__:
            if (s in path) and (t in path):
                return True
        return False

    def __reset_stored_paths__(self):
        self.__stored_paths__ = []

    def __increment_caller_id__(self):
        self._ID += 1

    def __get_called_id__(self):
        return '__{}__'.format(self._ID)


class NetlistSimplifier(__NetlistSimplifier__):

    @property
    def master_nodes(self):
        """ Excludes via devices with only two edges (series). """
        pass

    @property
    def branch_nodes(self):
        """ Nodes that defines different conducting branches. """
        branch_nodes = list()
        for n in self.g.nodes():
            if 'device' in self.g.node[n]:
                # if isinstance(self.g.node[n]['device'], spira.Dummy):
                #     branch_nodes.append(n)
                D = self.g.node[n]['device']
                if issubclass(type(D), (__Port__, spira.SRef)):
                    branch_nodes.append(n)
        return branch_nodes

    def detect_dummy_nodes(self):

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            s = self.branch_nodes[0]
            paths = []
            for t in filter(lambda x: x not in [s], self.branch_nodes):
                if nx.has_path(self.g, s, t):
                    for p in nx.all_simple_paths(self.g, source=s, target=t):
                        paths.append(p)

            new_paths = []
            for p1 in paths:
                for p2 in filter(lambda x: x not in [p1], paths):
                    set_2 = frozenset(p2)
                    intersection = [x for x in p1 if x in set_2]
                    new_paths.append(intersection)

            dummies = set()
            for path in new_paths:
                p = list(path)
                dummies.add(p[-1])

            for d in dummies:
                N = self.g.nodes[d]['device']
                if isinstance(N, spira.Label):
                    self.g.nodes[d]['device'] = spira.Dummy(
                        name='Dummy',
                        midpoint=N.position,
                        color='#90EE90'
                    )

    def generate_branches(self):
        """  """

        self.__reset_stored_paths__()
        self.__increment_caller_id__()
        text = self.__get_called_id__()

        for sg in nx.connected_component_subgraphs(self.g, copy=True):
            for s in self.branch_nodes:
                targets = filter(lambda x: x not in [s], self.branch_nodes)
                for t in targets:
                    self.__store_branch_paths__(s, t)
            for i, path in enumerate(self.__stored_paths__):

                source = self.g.node[path[-1]]['device'].__str__()

                for n in path[1:-1]:
                    lbl = self.g.node[n]['surface']
                    self.g.node[n]['device'] = spira.Label(
                    # self.g.node[n]['path'] = spira.Label(
                        position=lbl.position,
                        # text='path',
                        text=text,
                        gdslayer=lbl.gdslayer,
                        color='#FFFFFF',
                        node_id='{}_{}'.format(i, source)
                    )

        self.__remove_nodes__()

        return self.g

