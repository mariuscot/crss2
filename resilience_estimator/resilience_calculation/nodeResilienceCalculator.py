"""Calculate resilience on custom ResNodes in parent-before-child order."""

from graphlib import TopologicalSorter
from math import isfinite, prod

if __package__:
    from . import resilienceDependencyGraph
    from .configuration import configuration
else:
    import resilienceDependencyGraph
    from configuration import configuration

#Return {DOT node ID: calculated ResNode} for the whole directed graph.
#    cve is (score, CVE identifier); mop is a protection fraction in [0, 1]
#    applied at each node. Every root (including an isolated node) is treated
#    as an entry point. A child is calculated only after ALL its parents.
#    Cyclic graphs raise graphlib.CycleError because they have no such order.
#    realizedImpact is a loss fraction; resilienceValue = R0 * (1 - impact).

def calculateNodeResilienceForGraph(graph, R0, cve, mop):
    _validate_inputs(cve, R0, mop)
    children, nodesMap, parents, edgesMap = resilienceDependencyGraph.get_dependency_graph(graph, R0)
    # Compute the entire order first so a cycle fails before any calculation.
    order = list(TopologicalSorter(parents).static_order())

    for node_id in order:
        node = nodesMap[node_id]
        if not parents[node_id]:
            # This is an entry point; calculate its realized impact directly.
            # both EXP and SENS are set to 1.0 for maximum impact, scaled by the protection fraction (mop).
            node.realizedImpact = _entry_point_impact(cve, mop, EXP=1.0, SENS=1.0)
        else:
            # Each incoming edge contributes its parent's already computed loss.
            surviving_fractions = []
            for parent_id in parents[node_id]:
                parent = nodesMap[parent_id]
                edge = edgesMap[parent_id, node_id]
                layer_coupling, goal_coupling = getCouplingStrength(edge)
                applicability, containment = getApplicabilityAndContainment(edge)
                strength = applicability * layer_coupling * goal_coupling * containment
                surviving_fractions.append(1 - strength * parent.realizedImpact)
            node.realizedImpact = (1 - mop) * (1 - prod(surviving_fractions))

        node.resilienceValue = R0 * (1 - node.realizedImpact)
        node.participating = True

    return nodesMap


def _validate_inputs(cve, R0, mop):
    if not isinstance(cve, (tuple, list)) or len(cve) != 2:
        raise ValueError("cve must be (score, CVE identifier), e.g. (7.5, 'CVE-2014-0160')")
    for name, value, upper in (("CVE score", cve[0], 10), ("R0", R0, 1), ("mop", mop, 1)):
        if not isinstance(value, (int, float)) or not isfinite(value) or not 0 <= value <= upper:
            raise ValueError(f"{name} must be a finite number between 0 and {upper}")


# Full exposure and sensitivity; a higher score means greater damage.
# we selected the highest values for Exposure and Sensitivity for greatest impact. The impact is scaled by the protection fraction (mop) to give the realized impact.
def _entry_point_impact(cve, mop, EXP=1.0, SENS=1.0):
    TechSev = cve[0] / 10
    return TechSev * (1 - mop)


#Read plain edge attributes; missing types retain the original (1, 1) default.
# A 1:1 coupling between the different segements menas that effects potentially fully propagate from this perspective
def calculateEntryPointResilience(cve, R0, mop):
    _validate_inputs(cve, R0, mop)
    return R0 * (1 - _entry_point_impact(cve, mop))


#The return of this function gives the goal_coupling and layer_coupling for each of the IT /OT combinations """
def getCouplingStrength(edge):
    strengths = configuration.LAYER_GOAL_COUPLING_STRENGTHS
    edge_type = edge.get("type")
    if edge_type is None:
        return 1.0, 1.0
    if edge_type not in strengths:
        raise ValueError(f"Unknown edge type: {edge_type!r}")
    return strengths[edge_type]


#The applicability containmnet limits the propagation strength for different action types, modelling the edges of the graph """
def getApplicabilityAndContainment(edge):
    transitions = configuration.APPLICABILITY_CONTAINMENT_TRANSITIONS
    link = edge.get("link", "state")
    if link not in transitions:
        raise ValueError(f"Unknown edge link: {link!r}")
    return transitions[link]
