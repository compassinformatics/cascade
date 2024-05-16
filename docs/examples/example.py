from wayfarer import loader
from cascade import orderer

# load a network
net = loader.load_network_from_file("./docs/examples/40_directed_net.dat")
o = orderer.Orderer(code_field="EDGE_ID")

# assign orders to the network
orders = o.assign_order(net)

print(f"Number of edges with an order: {len(orders)}")

# loop through orders
for edge_id, values in list(orders.items())[0:10]:
    strahler_order, shreve_order = values[0], values[1]
    print(
        f"EdgeId: {edge_id} Strahler Order: {strahler_order} Shreve Order: {shreve_order}"
    )

# get a Strahler order for a specific edge
edge_id = 197
print(orders[197])
# orders is a dictionary using the edge id as a key, and values as a list in the
# following format
# strahler_stream_orders shreve_stream_orders segments visited
# [1, 1, 100007, 9]

strahler_order = orders[197][0]
print(f"Strahler order for {edge_id}: {strahler_order}")
