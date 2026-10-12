from dataclasses import replace
import math
from pathlib import Path

if __package__:
    from . import ahpEstimator, nodeResilienceCalculator, resilienceDependencyGraph, resilienceWeights, resilienceObjectives, sensitivityAnalysis
    from .configuration import configuration, parameters
    from .configuration.parameters import ResNode
else:
    from configuration import configuration, parameters
    from configuration.parameters import ResNode
    import ahpEstimator
    import nodeResilienceCalculator
    import resilienceDependencyGraph
    import resilienceWeights
    import resilienceObjectives
    import sensitivityAnalysis


def initializeResilienceMatrix(no_of_components, layers, goals, r0, compTypes):
    """Create baseline nodes at [component position][layer position][goal position].

    Stored compId values are 1..no_of_components, matching the graph metadata.
    layers and goals are enum collections, not integer counts.
    """
    layers, goals = list(layers), list(goals)
    if no_of_components < 0 or len(compTypes) != no_of_components:
        raise ValueError("Provide exactly one component type per component")

    res_nodes = []
    node_id = 0
    for comp_index in range(no_of_components):
        component_nodes = []
        for layer in layers:
            layer_nodes = []
            for goal in goals:
                node_id += 1
                layer_nodes.append(ResNode(
                    id=node_id, layer=layer, goal=goal,
                    compId=comp_index + 1, compType=compTypes[comp_index],
                    direction=0, resilienceValue=r0,
                    realizedImpact=float("nan"), participating=False,
                ))
            component_nodes.append(layer_nodes)
        res_nodes.append(component_nodes)
    return res_nodes


#Keep one node per (component, layer, goal), choosing minimum resilience.
#
#Copy the winning node so neither direction's input objects are modified.
#Its impact and direction stay paired with its resilience. Ties keep the
#first encountered node (direct before inverse in calcResilience).

def mergeResilienceResults(results):
    merged = {}
    for nodesMap in results.values():
        for node in nodesMap.values():
            key = (node.compId, node.layer, node.goal)
            if key not in merged or node.resilienceValue < merged[key].resilienceValue:
                merged[key] = replace(node)
    return merged


#Update the initialized matrix in place and return it.
#
#Preserve each cell's unique ID, component ID/type, layer and goal.
#Only calculated fields are copied; all other cells retain their baseline.

def populateResilienceMatrix(res_nodes, merged):
    cells = {
        (node.compId, node.layer, node.goal): node
        for component_nodes in res_nodes
        for layer_nodes in component_nodes
        for node in layer_nodes
    }
    missing = merged.keys() - cells.keys()
    if missing:
        raise ValueError(f"Calculated nodes are outside the initialized matrix: {missing}")

    for key, result in merged.items():
        cell = cells[key]
        cell.resilienceValue = result.resilienceValue
        cell.realizedImpact = result.realizedImpact
        cell.direction = result.direction
        cell.participating = result.participating
    return res_nodes


def calcResilience(cve=(7.5, "CVE-2014-0160"), R0=1.0, mop=0.0,
                   no_of_components=3, compTypes=(1, 2, 3), protection = 0):
    #Return the full matrix populated with minimum resilience across directions."""
    # Include every defined layer (currently five, including firmware) and goal.
    # Component types: 1 = IT system, 2 = LAN, 3 = OT system.
    res_nodes = initializeResilienceMatrix(
        no_of_components, parameters.Layers, parameters.Goals, R0, compTypes
    )
    results = {}
    for name, direction in (("direct", 1), ("inverse", 2)):
        graph = resilienceDependencyGraph.buildDependencyGraph_traversingPath(cve[1], direction, protection)
        if graph is not None:
            results[name] = (
                nodeResilienceCalculator.calculateNodeResilienceForGraph(graph, R0, cve, mop)
        )
    merged = mergeResilienceResults(results)
    return populateResilienceMatrix(res_nodes, merged)


#Calculate aggregated resilience value per layer using weighted aggregation.

#Aggregates resilience across all components and goals for each layer using
#weights from the specified expert's weight matrix. Skips non-participating nodes
#and nodes with NaN resilience values.

#input:
#    res_nodes: 3D matrix of ResNode objects [component_index][layer_index][goal_index]
#    resilience_weights_obj: ResilienceWeights object containing weight matrices
#    expert_number: Which expert's weights to use (1-4, default=1)
#    
#returns:
#    dict: Mapping of Layers enum to weighted resilience values
#            e.g., {Layers.HW: 0.75, Layers.FW: 0.68, ...}

def calculateLayerResilience(res_nodes, weights):
            
    # Initialize result dictionary for each layer
    layer_resilience = {layer: 0.0 for layer in parameters.Layers}
    layer_counts = {layer: 0 for layer in parameters.Layers}
    
    # Iterate through all nodes to aggregate resilience per layer
    for comp_index, component_nodes in enumerate(res_nodes):
        comp_type = res_nodes[comp_index][0][0].compType  # All nodes in component have same type
        comp_type_idx = comp_type - 1  # Convert from 1-based to 0-based indexing
        
        for layer_index, layer_nodes in enumerate(component_nodes):
            layer = layer_nodes[0].layer  # All nodes in layer have same layer enum
            
            for goal_index, node in enumerate(layer_nodes):
                # Skip non-participating nodes and nodes with NaN resilience values
#                if not node.participating or math.isnan(node.resilienceValue):
#                    continue
                
                # Get weight for this component, layer, and goal combination
                weight = weights[comp_type_idx][layer_index][goal_index]
                
                # Accumulate weighted resilience
                layer_resilience[layer] += node.resilienceValue * weight
                layer_counts[layer] += weight
    
    # Normalize by total weights per layer
    for layer in layer_resilience:
        if layer_counts[layer] > 0:
            # Resilience is already weighted, divide by sum of weights to get average
            layer_resilience[layer] /= layer_counts[layer]
    
    return layer_resilience

def calculateMilitaryLayerResilience(res_nodes, MMDM, weights):
            
    # Initialize result dictionary for each layer
    layer_resilience = {layer: 0.0 for layer in parameters.Layers}
    layer_counts = {layer: 0 for layer in parameters.Layers}
    
    # Iterate through all nodes to aggregate resilience per layer
    for comp_index, component_nodes in enumerate(res_nodes):
        comp_type = component_nodes[0][0].compType  # All nodes in component have same type
        comp_type_idx = comp_type - 1  # Convert from 1-based to 0-based indexing
        
        for layer_index, layer_nodes in enumerate(component_nodes):
            layer = layer_nodes[0].layer  # All nodes in layer have same layer enum
            
            for goal_index, node in enumerate(layer_nodes):
                # Skip non-participating nodes and nodes with NaN resilience values
                #if not node.participating or math.isnan(node.resilienceValue):
                #    continue
                
                # Get weight for this component, layer, and goal combination
                weight = weights[comp_type_idx][layer_index][goal_index]
                MMDM_value = MMDM[comp_type_idx][layer_index][goal_index]

                # Accumulate weighted resilience
                layer_resilience[layer] += node.resilienceValue * weight / MMDM_value
                layer_counts[layer] += weight
    
    # Normalize by total weights per layer
    for layer in layer_resilience:
        if layer_counts[layer] > 0:
            # Resilience is already weighted, divide by sum of weights to get average
            layer_resilience[layer] /= layer_counts[layer]
    
    return layer_resilience


#Print layer resilience values in a formatted table.

def printLayerResilience(layer_resilience):

    print("\n" + "="*50)
    print("Layer Resilience Summary")
    print("="*50)
    print(f"{'Layer':<15} | {'Resilience':<15}")
    print("-"*50)
    for layer in parameters.Layers:
        value = layer_resilience.get(layer, float('nan'))
        print(f"{layer.value[0]:<15} | {value:>14.4f}")
    print("="*50)


#Calculate overall resilience value across all components, layers, and goals.
#    
#    Aggregates resilience across the entire system using weighted aggregation
#    from the specified expert's weight matrix. Only includes participating nodes
#    with valid (non-NaN) resilience values.
#    
#   inputs:
#        res_nodes: 3D matrix of ResNode objects [component_index][layer_index][goal_index]
#        resilience_weights_obj: ResilienceWeights object containing weight matrices
#        expert_number: Which expert's weights to use (1-4, default=1)
#        
#   Returns:
#        float: Overall weighted resilience value for the entire system

def calculateOverallResilience(res_nodes, resilience_weights_obj):
    
    # Initialize accumulators
    total_weighted_resilience = 0.0
    total_weight = 0.0
    
    # Iterate through all nodes to aggregate resilience across the entire system
    for comp_index, component_nodes in enumerate(res_nodes):
        comp_type = res_nodes[comp_index][0][0].compType  # All nodes in component have same type
        comp_type_idx = comp_type - 1  # Convert from 1-based to 0-based indexing
        
        for layer_index, layer_nodes in enumerate(component_nodes):
            for goal_index, node in enumerate(layer_nodes):
                # Skip non-participating nodes and nodes with NaN resilience values
                #if not node.participating or math.isnan(node.resilienceValue):
                #    continue
                
                # Get weight for this component, layer, and goal combination
                weight = resilience_weights_obj[comp_type_idx][layer_index][goal_index]
                
                # Accumulate weighted resilience
                total_weighted_resilience += node.resilienceValue * weight
                total_weight += weight
    
    # Calculate overall resilience as weighted average
    if total_weight > 0:
        overall_resilience = total_weighted_resilience / total_weight
    else:
        overall_resilience = float('nan')
    
    return overall_resilience

#Calculate overall military resilience value across all components, layers, and goals.
def calculateOverallMilitaryResilience(res_nodes, resilience_weights_obj, MMDM):
    
    # Initialize accumulators
    total_weighted_resilience = 0.0
    total_weight = 0.0
    
    # Iterate through all nodes to aggregate resilience across the entire system
    for comp_index, component_nodes in enumerate(res_nodes):
        comp_type = res_nodes[comp_index][0][0].compType  # All nodes in component have same type
        comp_type_idx = comp_type - 1  # Convert from 1-based to 0-based indexing
        
        for layer_index, layer_nodes in enumerate(component_nodes):
            for goal_index, node in enumerate(layer_nodes):
                # Skip non-participating nodes and nodes with NaN resilience values
                #if not node.participating or math.isnan(node.resilienceValue):
                #    continue
                
                # Get weight for this component, layer, and goal combination
                weight = resilience_weights_obj[comp_type_idx][layer_index][goal_index]
                MMDM_value = MMDM[comp_type_idx][layer_index][goal_index]
                
                # Accumulate weighted resilience
                total_weighted_resilience += node.resilienceValue * weight / MMDM_value
                total_weight += weight
    
    # Calculate overall resilience as weighted average
    if total_weight > 0:
        overall_mil_resilience = total_weighted_resilience / total_weight
    else:
        overall_mil_resilience = float('nan')
    
    return overall_mil_resilience

#Print overall system resilience value.
#    
#  inputs: overall_resilience: Overall resilience value
#           expert_number: Which expert's weights were used
def printOverallResilience(overall_resilience, expert_number=1):
    print("\n" + "="*50)
    print(f"Overall System Resilience (Expert {expert_number})")
    print("="*50)
    print(f"Overall Resilience: {overall_resilience:>14.4f}")
    print("="*50)


def calcNodeResilience (mop_factor):
    # calculate resilience matrix
    res_nodes = calcResilience(mop = mop_factor)

    print("\nMerged resilience matrix, protection is: ", mop_factor)
    for component_nodes in res_nodes:
        for layer_nodes in component_nodes:
            for node in layer_nodes:
                print(
                    f"C{node.compId} {node.layer.name}/{node.goal.name}: "
                    f"resilience={node.resilienceValue:.6f}, "
                    f"impact={node.realizedImpact:.6f}, participating={node.participating}"
                )

    return res_nodes

def calculateResilienceWeights(oppinion_specialists):
    weights_obj = resilienceWeights.ResilienceWeights()
    average_weights = weights_obj.get_average_weights(oppinion_specialists)
    estimated_weights, crArray = ahpEstimator.conduct_ahp_analysis_overall(average_weights)

    return estimated_weights, crArray

def calcCivilianResilience(res_nodes):
    estimated_weights, crArray = calculateResilienceWeights(oppinion_specialists=[0.4, 0.15, 0.25, 0.2])

    layer_resilience = calculateLayerResilience(res_nodes=res_nodes, weights=estimated_weights)

    civilian_resilience = calculateOverallResilience(
        res_nodes=res_nodes,
        resilience_weights_obj=estimated_weights,
    )

    return civilian_resilience, layer_resilience

def calcMilitaryResilience(
    res_nodes,
    civilian_resilience,
    layer_resilience,
    MT=0.8,
    MO=0.6,
    sensitivity_increment=0.05):
    # 5% variation allowed in initial weights

    MMDM, sensitivity_results = build_MMDM(MT, MO, sensitivity_increment)

    estimated_weights, crArray = calculateResilienceWeights(oppinion_specialists=[0.4, 0.15, 0.25, 0.2])

    mil_layer_resilience = calculateMilitaryLayerResilience(
        res_nodes=res_nodes,
        MMDM=MMDM,
        weights=estimated_weights,
    )

    military_resilience = calculateOverallMilitaryResilience(
        res_nodes=res_nodes,
        resilience_weights_obj=estimated_weights,
        MMDM=MMDM,
    )

    return military_resilience, mil_layer_resilience, sensitivity_results


#Build the military mission capability matrix and weight sensitivities.
# Returns the baseline MMDM and a dictionary with one-at-a-time sensitivity scenarios for WMC, WMOS, and WIM.
def build_MMDM(MT, MO, sensitivity_increment):
    initial_weights = configuration.MMCM_INITIAL_WEIGHTS
    weight_names = ("WMC", "WMOS", "WIM")
    normalized_objectives = (
        resilienceObjectives.ResilienceObjectives().get_normalized_objectives_matrix()
    )

    def build_MMDM(weights):
        wmc, wmos, wim = weights
        return 1 + MT * wmc + MO * wmos + wim * normalized_objectives

    MMDM = build_MMDM(initial_weights)
    sensitivity_results = {}
    for weight_index, weight_name in enumerate(weight_names):
        perturbed_weights, redistribution_ratio = sensitivityAnalysis.increaseweights(
            initial_weights, weight_index, sensitivity_increment
        )
        sensitivity_results[weight_name] = {
            "weights": perturbed_weights,
            "redistribution_ratio": redistribution_ratio,
            "MMDM": build_MMDM(perturbed_weights),
        }

    return MMDM, sensitivity_results

def resilienceCalculatorForCVE(cve=(7.5, "CVE-2014-0160"), R0 = 1.0, mop = 0, protection= 0, MT=0.1, MO=0.2):
    compTypes=(1, 2, 3)
    no_of_components=3
    res_nodes = calcResilience(cve, R0, mop ,no_of_components, compTypes, protection)

    # calculate civilian resilience
    civilian_resilience, civ_layer_resilience = calcCivilianResilience(res_nodes)

    # calculate military resilience
    military_resilience, mil_layer_resilience, sensitivity_results = calcMilitaryResilience(res_nodes, civilian_resilience, civ_layer_resilience,  MT, MO)

    return res_nodes, civilian_resilience, civ_layer_resilience, military_resilience, mil_layer_resilience


def write_resilience_report(
    report_path,
    cve_name,
    protection_name,
    civilian_resilience,
    civ_layer_resilience,
    military_resilience,
    mil_layer_resilience,
    civ_layer_levels,
    mil_layer_levels,
):
    lines = [
        f"CVE: {cve_name}",
        f"Scenario: {protection_name}",
        "Civilian Layer Resilience:",
    ]
    for layer in parameters.Layers:
        value = civ_layer_resilience.get(layer, float('nan'))
        level = civ_layer_levels.get(layer, "N/A")
        lines.append(f"  {layer.value[0]}: {value:.6f} ({level})")
    lines.append(f"Civilian Overall Resilience: {civilian_resilience:.6f}")
    lines.append("")
    lines.append("Military Layer Resilience:")
    for layer in parameters.Layers:
        value = mil_layer_resilience.get(layer, float('nan'))
        level = mil_layer_levels.get(layer, "N/A")
        lines.append(f"  {layer.value[0]}: {value:.6f} ({level})")
    lines.append(f"Military Overall Resilience: {military_resilience:.6f}")
    lines.append("")

    with report_path.open("a", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines) + "\n")

#Write the civilian resilience of each node to file, grouped by component, layer, and goal.
def write_civilian_node_resilience_report(report_path, cve_name, protection_name, res_nodes, weights=None):
    if weights is None:
        weights, _ = calculateResilienceWeights([0.4, 0.15, 0.25, 0.2])

    lines = [
        f"CVE: {cve_name}",
        f"Scenario: {protection_name}",
        "Civilian resilience by node (component / layer / goal):",
        "component | layer | goal | resilience | weight | node_id",
    ]

    for comp_index, component_nodes in enumerate(res_nodes, start=1):
        for layer_index, layer_nodes in enumerate(component_nodes):
            layer = layer_nodes[0].layer
            for goal_index, node in enumerate(layer_nodes):
                comp_type_idx = node.compType - 1
                weight = weights[comp_type_idx][layer_index][goal_index]
                lines.append(
                    f"{comp_index:>9} | {layer.value[0]:>8} | {node.goal.name:<5} | "
                    f"{node.resilienceValue:>10.6f} | {weight:>8.6f} | {node.id:>5}"
                )

    lines.append("")
    with report_path.open("a", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines) + "\n")
