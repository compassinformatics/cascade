import networkx as nx
from cascade import orderer
from wayfarer import loader


def make_simple_network():
    r"""

    A network similar to below (flow to left):
         D
         /
      B /\
    ___/  C
    A  \
       E\/ F
         \ G

    """
    G = nx.DiGraph()

    nodes = [1, 2, 3, 4, 5, -3, -4, -5]

    for n in nodes:
        G.add_node(n)

    # print(G.nodes())
    G.add_edge(2, 1, **{"SEG_CD": "A"})

    # top half
    G.add_edge(3, 2, **{"SEG_CD": "B"})
    G.add_edge(4, 3, **{"SEG_CD": "C"})
    G.add_edge(5, 3, **{"SEG_CD": "D"})

    # bottom half
    G.add_edge(-3, 2, **{"SEG_CD": "E"})
    G.add_edge(-4, -3, **{"SEG_CD": "F"})
    G.add_edge(-5, -3, **{"SEG_CD": "G"})

    return G


def make_looped_network():
    r"""

    A network similar to below (flow to left):

         / C
      B /\ D
    ___/  \___ 6
    A  \  /  E
       F\/ G

    """
    G = nx.DiGraph()

    nodes = [1, 2, 3, 4, 5, 6, 7]

    for n in nodes:
        G.add_node(n)

    G.add_edge(2, 1, **{"SEG_CD": "A"})
    G.add_edge(3, 2, **{"SEG_CD": "B"})
    G.add_edge(4, 3, **{"SEG_CD": "C"})
    G.add_edge(5, 3, **{"SEG_CD": "D"})
    G.add_edge(6, 5, **{"SEG_CD": "E"})
    G.add_edge(-3, 2, **{"SEG_CD": "F"})
    G.add_edge(5, -3, **{"SEG_CD": "G"})

    return G


def test_get_dicts():

    net = make_simple_network()

    o = orderer.Orderer()
    originating_node, from_nodes_per_arc, inflowing_arcs_per_node = o.make_dicts(net)

    assert originating_node == {
        "A": 2,
        "C": 4,
        "B": 3,
        "E": -3,
        "D": 5,
        "G": -5,
        "F": -4,
    }
    assert from_nodes_per_arc == {
        "A": 2,
        "C": 4,
        "B": 3,
        "E": -3,
        "D": 5,
        "G": -5,
        "F": -4,
    }
    assert inflowing_arcs_per_node == {
        1: ["A"],
        2: ["B", "E"],
        3: ["C", "D"],
        4: [],
        5: [],
        -5: [],
        -4: [],
        -3: ["F", "G"],
    }


def test_get_looped_dicts():

    net = make_looped_network()

    o = orderer.Orderer()
    originating_node, from_nodes_per_arc, inflowing_arcs_per_node = o.make_dicts(net)

    assert originating_node == {
        "A": 2,
        "C": 4,
        "B": 3,
        "E": 6,
        "D": 5,
        "G": 5,
        "F": -3,
    }

    assert from_nodes_per_arc == {
        "A": 2,
        "C": 4,
        "B": 3,
        "E": 6,
        "D": 5,
        "G": 5,
        "F": -3,
    }

    exp = {
        1: ["A"],
        2: ["B", "F"],
        3: ["C", "D"],
        4: [],
        5: ["E"],
        6: [],
        7: [],
        -3: ["G"],
    }

    assert inflowing_arcs_per_node == exp


def test_get_dicts_full_network():

    single_network = "./tests/data/HydroNetwork03.pickled"
    net = loader.load_network_from_file(single_network)

    o = orderer.Orderer()
    originating_node, from_nodes_per_arc, inflowing_arcs_per_node = o.make_dicts(net)

    from_nodes = from_nodes_per_arc["03_422"]
    assert from_nodes == (274478.11278015375, 341127.9601954147)
    assert 1012 == len(originating_node)
    assert 1012 == len(from_nodes_per_arc)
    assert 1021 == len(inflowing_arcs_per_node)


def test_get_strahler_order():

    o = orderer.Orderer()

    up_orders = [(2, 3), (1, 6)]
    max_order_origin, max_order_count, max_order = o.get_strahler_order(up_orders)

    assert 3 == max_order_origin
    assert 1 == max_order_count
    assert 2 == max_order


def test_assign_order():

    single_network = "./tests/data/HydroNetwork03.pickled"
    net = loader.load_network_from_file(single_network)

    o = orderer.Orderer()

    orders = o.assign_order(net)

    assert 5 == orders["03_422"][0]

    assert 1012 == len(orders)  # one order for every segment


def test_merge_result_dicts():

    single_network = "./tests/data/HydroNetwork03.pickled"
    net = loader.load_network_from_file(single_network)

    o = orderer.Orderer()

    orders = o.assign_order(net)

    # returns the following values
    # strahler_stream_orders shreve_stream_orders segments visited
    assert orders["03_422"] == [5, 152, 500002, 609]
    assert 1012 == len(orders)  # one order for every segment


def xtest_assign_order_loops_full():
    """
    Test on a network with loops

    ['GBNI0200142', 'GBNI0201298', 'GBNI0201300', 'GBNI0201318', 'GBNI0201217', 'GBNI0200035', 'GBNI0201092']
    ['GBNI0200142', 'GBNI0201298', 'GBNI0201300', 'GBNI0201318', 'GBNI0201217', 'GBNI0200035', 'GBNI0201092']
    """

    single_network_loops = "./tests/data/HydroNetwork01_02_40.pickled"
    net = loader.load_network_from_file(single_network_loops)

    o = orderer.Orderer()

    full_network_orders = o.assign_order(net)

    assert full_network_orders == (3, 4)

    assert 6936 == len(full_network_orders)  # one order for every segment


def test_order_simple_network():
    """
    Test on a simple network
    """

    o = orderer.Orderer()

    arc_id = "A"

    originating_node = {"A": 2, "C": 4, "B": 3, "E": -3, "D": 5, "G": -5, "F": -4}
    from_nodes_per_arc = {"A": 2, "C": 4, "B": 3, "E": -3, "D": 5, "G": -5, "F": -4}
    inflowing_arcs_per_node = {
        1: ["A"],
        2: ["B", "E"],
        3: ["C", "D"],
        4: [],
        5: [],
        -5: [],
        -4: [],
        -3: ["G", "F"],
    }

    o.create_globals()

    full_network_orders = o.order_network(
        arc_id, from_nodes_per_arc, inflowing_arcs_per_node, originating_node
    )

    assert full_network_orders == (3, 4)

    assert o.strahler_stream_orders == {
        "A": 3,
        "C": 1,
        "B": 2,
        "E": 2,
        "D": 1,
        "G": 1,
        "F": 1,
    }

    assert o.shreve_stream_orders == {
        "A": 4,
        "C": 1,
        "B": 2,
        "E": 2,
        "D": 1,
        "G": 1,
        "F": 1,
    }

    assert originating_node == {
        "A": 2,
        "C": 4,
        "B": 3,
        "E": -3,
        "D": 5,
        "G": -5,
        "F": -4,
    }

    assert o.visited == {"A": 0, "C": 2, "B": 1, "E": 4, "D": 3, "G": 5, "F": 6}

    assert o.segment_ids_per_originating_node == {
        2: 300001,
        3: 200001,
        4: 100001,
        5: 100002,
        -5: 100003,
        -4: 100004,
        -3: 200002,
    }

    assert o.segments == {
        "A": 300001,
        "C": 100001,
        "B": 200001,
        "E": 200002,
        "D": 100002,
        "G": 100003,
        "F": 100004,
    }

    assert 7 == len(o.visited.keys())


def test_order_network_loops():
    """
    Test on a network with loops
    """

    o = orderer.Orderer()

    arc_id = "A"

    from_nodes_per_arc = {"A": 2, "C": 4, "B": 3, "E": 6, "D": 5, "G": 5, "F": -3}
    originating_node = {"A": 2, "C": 4, "B": 3, "E": 6, "D": 5, "G": 5, "F": -3}

    inflowing_arcs_per_node = {
        1: ["A"],
        2: ["B", "F"],
        3: ["C", "D"],
        4: [],
        5: ["E"],
        6: [],
        7: [],
        -3: ["G"],
    }

    o.create_globals()

    full_network_orders = o.order_network(
        arc_id, from_nodes_per_arc, inflowing_arcs_per_node, originating_node
    )

    assert full_network_orders == (2, 3)

    assert o.strahler_stream_orders == {
        "A": 2,
        "C": 1,
        "B": 2,
        "E": 1,
        "D": 1,
        "G": 1,
        "F": 1,
    }

    # not sure how this is meant to work - should duplicate upstream be added twice?
    assert o.shreve_stream_orders == {
        "A": 3,
        "C": 1,
        "B": 2,
        "E": 1,
        "D": 1,
        "G": 1,
        "F": 1,
    }

    assert originating_node == {
        "A": 3,
        "C": 4,
        "B": 3,
        "E": 6,
        "D": 6,
        "G": 6,
        "F": 6,
    }

    assert o.visited == {"A": 0, "C": 2, "B": 1, "E": 4, "D": 3, "G": 6, "F": 5}

    assert o.segment_ids_per_originating_node == {3: 200001, 4: 100001, 6: 100002}

    # print(o.segments)
    assert o.segments == {
        "A": 200001,
        "C": 100001,
        "B": 200001,
        "E": 100002,
        "D": 100002,
        "G": 100002,
        "F": 100002,
    }

    assert 7 == len(o.visited.keys())
