import fiona
from networkx import MultiDiGraph
from wayfarer import loader
from cascade import orderer

# load a network from a shapefile
recs = fiona.open("./docs/examples/HydroEdge11.shp", "r")
net = loader.load_network_from_geometries(
    recs,
    key_field="SEG_CD",
    keep_geometry=True,
    use_integer_keys=False,
    graph_type=MultiDiGraph,
)
o = orderer.Orderer(code_field="SEG_CD")

# assign orders to the network
orders = o.assign_order(net)

# loop through orders
for seg_cd, values in orders.items():
    strahler_order, shreve_order = values[0], values[1]
    print(
        f"Segment Code: {seg_cd} Strahler Order: {strahler_order} Shreve Order: {shreve_order}"
    )
