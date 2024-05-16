from __future__ import annotations
import logging
from collections import defaultdict
from wayfarer import functions
import networkx
from networkx import DiGraph, MultiDiGraph

log = logging.getLogger("cascade")


class Orderer(object):

    def __init__(self, code_field: str = "SEG_CD"):
        self.code_field = code_field

    def make_dicts(
        self, net: DiGraph | MultiDiGraph, code_field: str | None = None
    ) -> tuple[dict, dict, dict]:
        """
        For braided networks the preprocessing procedure should create an
        InflowingArcsPerNode dictionary (instead of an ArcsPerNode dictionary) that would contain for every
        node only those arcs that flow into that same node. It should also create a FromNodesPerArc dictionary
        (instead of a NodesPerArc dictionary) to contain the from- nodes of each arc.
        """

        if not code_field:
            code_field = self.code_field

        from_nodes_per_arc = {}
        inflowing_arcs_per_node: dict = {}
        originating_node = {}  # Lanfear property - this dict is updated during ordering

        # make empty lists for all nodes
        for node in net.nodes():
            inflowing_arcs_per_node[node] = []

        for edge in net.edges(data=True):

            # for every edge
            seg_cd = edge[2][code_field]

            from_nodes_per_arc[seg_cd] = edge[0]
            originating_node[seg_cd] = edge[0]

            for node in net.nodes():
                if node == edge[1]:  # end node
                    inflowing_arcs_per_node[node].append(seg_cd)

        return originating_node, from_nodes_per_arc, inflowing_arcs_per_node

    def get_strahler_order(
        self, up_orders: list[tuple[int, int]]
    ) -> tuple[int, int, int]:
        """
        up_orders is a list of tuples containing (order, origin_node)

        e.g. [(2, 3), (1, 6)]

        Returns:

        max_order_origin - the id of the node
        max_order_count - the number of tuples with the maximum order
        max_order - the maximum order in the list
        """

        max_order = 0
        max_order_count = 0
        max_order_origin = 0

        for order, origin in up_orders:
            if order > max_order:
                max_order = order
                max_order_count += 1
                max_order_origin = origin
            elif order == max_order:
                if origin != max_order_origin:
                    max_order_count += 1

        return max_order_origin, max_order_count, max_order

    def create_ids_array(self) -> list[int]:

        # assume maximum river order of 15
        segment_ids = list(map(lambda x: x * 100000, range(0, 15)))

        return segment_ids

    def order_network(
        self,
        arc_id: int,
        from_nodes_per_arc: dict,
        inflowing_arcs_per_node: dict,
        originating_node: dict,
        count: int = 0,
    ) -> tuple[int, int]:
        """

        Based on `create_file.py <https://github.com/sahg/PyTOPKAPI/blob/master/pytopkapi/parameter_utils/create_file.py>`_ (BSD license)
        See `PyTOPKAPI Documentation <http://sahg.github.io/PyTOPKAPI/>`_ for more details

        Calculate the Strahler stream order

        This function recursively computes the Strahler stream order using
        the algorithm described by Gleyzer et al. (2004). The sequence of
        stream orders for the starting arc and each upstream arc is
        returned in the dictionary `stream_orders`.

        This also introduces the concept of river segments - collections of arcs of the same order

        + originating_node is used to keep track of the node at the top of the path
        + segments - an empty Segments dictionary, global to the procedure, is assumed to be created before
          execution of the procedure. This dictionary will hold the actual segment ID for each network arc.
        """
        # import traceback
        # print(count, arc_id, len(traceback.format_stack()))
        count += 1
        self.visited[arc_id] = len(self.visited)

        from_nodes = from_nodes_per_arc[arc_id]
        in_segments = inflowing_arcs_per_node[from_nodes]

        if len(in_segments) == 0:
            # only one edge so set order to 1
            shreve_order, strahler_order = 1, 1
            self.strahler_stream_orders[arc_id] = strahler_order
            self.shreve_stream_orders[arc_id] = shreve_order
        else:
            upstream_orders = {}

            for arc in in_segments:
                if arc not in self.visited:
                    strahler_order, shreve_order = self.order_network(
                        arc,
                        from_nodes_per_arc,
                        inflowing_arcs_per_node,
                        originating_node,
                        count,
                    )
                    origin = originating_node[arc]
                    upstream_orders[arc] = (strahler_order, shreve_order, origin)
                else:
                    origin = originating_node[arc]

                    if (
                        arc in self.strahler_stream_orders
                        and arc in self.shreve_stream_orders
                    ):
                        strahler_order, shreve_order = (
                            self.strahler_stream_orders[arc],
                            self.shreve_stream_orders[arc],
                        )
                    else:
                        strahler_order, shreve_order = 0, 0
                        self.errors.append(arc)

                    upstream_orders[arc] = (strahler_order, shreve_order, origin)

            # Shreve - add together all upstream orders
            shreve_order = sum([shreve for _, shreve, _ in upstream_orders.values()])
            self.shreve_stream_orders[arc_id] = shreve_order

            # Strahler
            up_orders = [
                (strahler, orig) for strahler, _, orig in upstream_orders.values()
            ]

            up_orders.sort(reverse=True)  # sort by stream order ascending
            max_order_origin, max_order_count, max_order = self.get_strahler_order(
                up_orders
            )

            if max_order_count > 1:
                # two upstream segments have the maximum order
                # so the segment order increases
                strahler_order = max_order + 1
                originating_node[arc_id] = from_nodes
            else:
                # otherwise it remains the same
                strahler_order = max_order
                originating_node[arc_id] = max_order_origin

            self.strahler_stream_orders[arc_id] = strahler_order

        current_origin_node = originating_node[arc_id]
        current_order = strahler_order

        if current_origin_node not in self.segment_ids_per_originating_node:
            # create a new segment id

            seg_id = self.segment_ids[current_order] + 1
            self.segment_ids[current_order] = seg_id

            self.segment_ids_per_originating_node[current_origin_node] = seg_id

        else:
            seg_id = self.segment_ids_per_originating_node[current_origin_node]

        self.segments[arc_id] = seg_id

        return strahler_order, shreve_order

    def create_globals(self):

        self.segment_ids = self.create_ids_array()
        self.strahler_stream_orders = {}
        self.shreve_stream_orders = {}
        self.visited = {}
        self.segment_ids_per_originating_node = {}
        self.segments = {}
        self.errors = []

    def merge_result_dicts(self) -> dict:

        dd = defaultdict(list)

        my_dicts = (
            self.strahler_stream_orders,
            self.shreve_stream_orders,
            self.segments,
            self.visited,
        )
        for d in my_dicts:  # you can list as many input dicts as you want here
            for key, value in d.items():
                dd[key].append(value)

        return dd

    def assign_order(
        self, net: DiGraph | MultiDiGraph, selected_keys: list[str | int] | None = None
    ) -> dict:
        """
        The new braided version can also easily deal with
        multiple drainage outlets. To address such cases, the
        procedure must be executed separately for each pour
        point (outlet) present in the network. When the proce-
        dure first reaches the 'split node,' where the network
        splits into multiple drainage paths, it will not follow
        the other paths, since they do not flow into that split
        node, but rather out of it. Then, in successive calls for
        other outlets, the procedure can use already deter-
        mined stream orders of the split node's upstream arcs
        instead of repeating that upstream part's traversal.
        Of course, all external dictionaries should be shared
        among the calls to maintain consistency among them
        """

        code_field = self.code_field

        sink_edges = functions.get_sink_edges(net)

        if selected_keys:
            # if a key error here then one of the selected_keys is not a sink
            sink_edges = {key: sink_edges[key] for key in selected_keys}

        self.create_globals()

        log.debug("%i sinks", len(sink_edges))

        for i, (sink_seg_cd, edge) in enumerate(sink_edges.items(), start=1):

            log.debug("Sink %s (%i / %i)", sink_seg_cd, i, len(sink_edges))

            # http://stackoverflow.com/questions/13914920/networkx-extract-the-smallest-connected-subgraph
            subnet = net.subgraph(
                networkx.shortest_path(net.to_undirected(), edge["NODEID_TO"])
            )

            originating_node, from_nodes_per_arc, inflowing_arcs_per_node = (
                self.make_dicts(subnet, code_field)
            )
            self.order_network(
                sink_seg_cd,
                from_nodes_per_arc,
                inflowing_arcs_per_node,
                originating_node,
            )

        return self.merge_result_dicts()
