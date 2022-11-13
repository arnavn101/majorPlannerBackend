import networkx as nx
from course_graph import return_good
from pyvis.network import Network
from collections import defaultdict
import matplotlib.pyplot as plt

_, adj_list = return_good(["Artificial Intelligence", "Systems"], [])
rev_adj_list = defaultdict(list)

for k, v_list in adj_list.items():
    for v in v_list:
        rev_adj_list[v].append(k)

nx_graph = nx.DiGraph(dict(rev_adj_list))

# nt = Network('250px', '250px', directed=True)
# nt.from_nx(nx_graph)
# nt.show('nx.html')

# pos = nx.spring_layout(nx_graph, k=0.8, iterations=20)
# nx.draw(nx_graph, pos, node_color='#A0CBE2', edge_color='#BB0000', width=2, edge_cmap=plt.cm.Blues, with_labels=True
#         , node_size=1000)
# plt.savefig("graph.png", dpi=1000)
