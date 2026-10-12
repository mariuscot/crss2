from graphviz import Digraph
import pydot

if __package__:
    from .configuration.parameters import Goals, Layers, ResNode
else:
    from configuration.parameters import Goals, Layers, ResNode

import sys
from pathlib import Path

# Make the sibling mygraphs package available when running a script directly.
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from mygraphs.CVE_2014_0160_radar_entry_one_way import (
    createOneWayGraph as createGraphCVE_2014_0160
)
from mygraphs.CVE_2014_0160_radar_entry_one_way import (
    createOneWayReverseGraph as createReverseGraphCVE_2014_0160
)
from mygraphs.CVE_2017_0144_radar_entry_one_way import (
    createOneWayGraph as createGraphCVE_2017_0144
)
from mygraphs.CVE_2017_0144_radar_entry_one_way import (
    createOneWayReverseGraph as createReverseGraphCVE_2017_0144
)

from mygraphs.CVE_2014_0160_radar_entry_one_way_protected import (
    createOneWayGraph as createGraphCVE_2014_0160_protected
)
from mygraphs.CVE_2014_0160_radar_entry_one_way_protected import (
    createOneWayReverseGraph as createReverseGraphCVE_2014_0160_protected
)
from mygraphs.CVE_2017_0144_radar_entry_one_way_protected import (
    createOneWayGraph as createGraphCVE_2017_0144_protected
)
from mygraphs.CVE_2017_0144_radar_entry_one_way_protected import (
    createOneWayReverseGraph as createReverseGraphCVE_2017_0144_protected
)

# build dependency graph from a dot file
# the top node is the entry point for the particular traversing direction
def buildDependencyGraph_traversingPath(cve, direction, protected):
    if direction not in (1, 2):
        raise ValueError("direction must be 1 (direct) or 2 (inverse)")
    if protected not in (0, 1):
        raise ValueError("protection must be 0 (not protected) or 1 (protected)")


    g = Digraph("Resilience", format="png")
    cve = str(cve).strip().upper()
    match cve:
        case 'CVE-2014-0160':
            if direction == 1:
                if protected == 0:
                    g, output_path, dot_path, svg_path = createGraphCVE_2014_0160()
                else:
                    g, output_path, dot_path, svg_path = createGraphCVE_2014_0160_protected()
            else:
                if protected == 0:
                    g, output_path, dot_path, svg_path = createReverseGraphCVE_2014_0160()
                else:
                    g, output_path, dot_path, svg_path = createReverseGraphCVE_2014_0160_protected()
        case 'CVE-2017-0144':
            if direction == 1:
                if protected == 0:
                    g, output_path, dot_path, svg_path = createGraphCVE_2017_0144()
                else:
                    g, output_path, dot_path, svg_path = createGraphCVE_2017_0144_protected()
            else:
                if protected == 0:
                    g, output_path, dot_path, svg_path = createReverseGraphCVE_2017_0144()
                else:
                    g, output_path, dot_path, svg_path = createReverseGraphCVE_2017_0144_protected()
        case _:
            raise ValueError(f"Unsupported CVE: {cve}")

    return g
    

def get_node_by_label(g, wanted_label):
    parsed_graph = pydot.graph_from_dot_data(g.source)[0]

    for node in parsed_graph.get_nodes():
        compId = clean_dot_value(node.get_attributes().get("compId"))
        goal = clean_dot_value(node.get_attributes().get("goal"))
        layer = clean_dot_value(node.get_attributes().get("layer"))

        label = f"{layer}{compId}_{goal}"       

        if label.casefold() == wanted_label.casefold():
            return node

    return None

def clean_dot_value(value):
    if value is None:
        return None
    return value.strip('"').replace(r"\n", "\n")

def collect(dot_graph, node_defaults=None, edge_defaults=None):
    edgesMap = {}
    node_attributes = {}

    node_defaults = dict(node_defaults or {})
    edge_defaults = dict(edge_defaults or {})
    for defaults in dot_graph.get_node_defaults():
        node_defaults.update(defaults)
    for defaults in dot_graph.get_edge_defaults():
        edge_defaults.update(defaults)
    for dot_node in dot_graph.get_nodes():
        if dot_node.get_name() in ("node", "edge", "graph", '"\\n"', '""'):
            continue
        node_id = clean_dot_value(dot_node.get_name())
        attributes = node_attributes.setdefault(node_id, dict(node_defaults))
        attributes.update(dot_node.get_attributes())
    for edge in dot_graph.get_edges():
        source = clean_dot_value(edge.get_source())
        target = clean_dot_value(edge.get_destination())
        if (source, target) in edgesMap:
            raise ValueError(f"Duplicate dependency edge: {source} -> {target}")
        attributes = {**edge_defaults, **edge.get_attributes()}
        edgesMap[source, target] = {
            key: clean_dot_value(value) for key, value in attributes.items()
        }
    for subgraph in dot_graph.get_subgraphs():
        collect(subgraph, node_defaults, edge_defaults)

    return edgesMap,node_attributes

"""Convert DOT once into children, ResNodes, parents and edge attributes.

All maps use the exact DOT node ID (e.g. APP1_Ant), never its display label (e.g. APPL1_ANT). 
Leaves and isolated nodes are included. pydot objects stay inside this conversion boundary.
"""
def get_dependency_graph(g, R0=1.0):
    parsed = pydot.graph_from_dot_data(g.source)[0]

    edgesMap, node_attributes = collect(parsed)
    nodesMap = {}
    for node_id, attributes in node_attributes.items():
        attributes = {key: clean_dot_value(value) for key, value in attributes.items()}
        try:
            nodesMap[node_id] = ResNode(
                id=len(nodesMap) + 1,
                layer=Layers[attributes["layer"].upper()],
                goal=Goals[attributes["goal"].upper()],
                compId=int(attributes["compId"]),
                compType=attributes["compType"],
                direction=int(attributes["direction"]),
                resilienceValue=R0,
                realizedImpact=float("nan"),
                participating=False,
                mop = 0
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise ValueError(f"Invalid or missing metadata for node {node_id!r}: {attributes}") from exc

    children = {node_id: [] for node_id in nodesMap}
    parents = {node_id: [] for node_id in nodesMap}
    for source, target in edgesMap:
        for node_id in (source, target):
            if node_id not in nodesMap:
                raise ValueError(f"Edge references undeclared node {node_id!r}; add its node metadata")
        children[source].append(target)
        parents[target].append(source)
    return children, nodesMap, parents, edgesMap


def get_adjacency_from_digraph(g, R0=1.0):
    """Return adjacency maps and custom ResNode objects, keyed by DOT IDs."""
    children, nodesMap, parents, _ = get_dependency_graph(g, R0)
    return children, nodesMap, parents

def main():
    m = buildDependencyGraph_traversingPath('CVE-2014-0160', 1, 0)
    children, nodes, parents = get_adjacency_from_digraph(m)
    print("Children", children)
    print("Nodes", nodes)
    print("Parents", parents)
    
if __name__ == "__main__":
    main()
