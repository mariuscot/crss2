import numpy as np


# Define resilience objectives as constants
class ResilienceObjectives:
    #Container for resilience objective matrices.
    
    #Resilience objectives: confidentiality, integrity, availability, survivability,
    #recoverability, degraded_operation, mission_continuity
    
    #The objectives follow the structure: [component_type, layer, goal]
    #- Component types: 0 (OT-control), 1 (LAN), 2 (OT-sensor)
    #- Layers: 0 (HW), 1 (FW), 2 (NETW), 3 (APPL)
    #- Goals: 0 (ANT), 1 (WITH), 2 (REC), 3 (ADPT)
    
    #Each cell contains a set of resilience objectives for that combination.
    #Contains 4 objective matrices representing opinions from 4 different experts.
    
    # Resilience objectives constants
    CONFIDENTIALITY = "confidentiality"
    INTEGRITY = "integrity"
    AVAILABILITY = "availability"
    SURVIVABILITY = "survivability"
    RECOVERABILITY = "recoverability"
    DEGRADED_OPERATION = "degraded_operation"
    MISSION_CONTINUITY = "mission_continuity"
    
    ALL_OBJECTIVES = {
        CONFIDENTIALITY, INTEGRITY, AVAILABILITY, SURVIVABILITY,
        RECOVERABILITY, DEGRADED_OPERATION, MISSION_CONTINUITY
    }
    
    def __init__(self):
        """Initialize objective matrices for 4 experts."""
        self.objectives_expert1 = self._create_expert1_objectives()
        self.objectives_expert2 = self._create_expert2_objectives()
        self.objectives_expert3 = self._create_expert3_objectives()
        self.objectives_expert4 = self._create_expert4_objectives()
        
        self.all_objectives = [
            self.objectives_expert1,
            self.objectives_expert2,
            self.objectives_expert3,
            self.objectives_expert4
        ]

    """ Expert 1 objectives: Focus on anticipation and prevention.
        Emphasizes confidentiality, integrity, and availability.  """
    def _create_expert1_objectives(self):
        objectives = [[[[set() for _ in range(4)] for _ in range(4)] for _ in range(3)]]
        
        # Component 0: OT-control
        # Layer 0: HW
        objectives[0][0][0][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][0][0][1] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY, self.SURVIVABILITY}
        objectives[0][0][0][2] = {self.RECOVERABILITY, self.AVAILABILITY}
        objectives[0][0][0][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        # Layer 1: FW
        objectives[0][0][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][0][1][1] = {self.CONFIDENTIALITY, self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][0][1][2] = {self.RECOVERABILITY}
        objectives[0][0][1][3] = {self.MISSION_CONTINUITY}
        
        # Layer 2: NETW
        objectives[0][0][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][0][2][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][0][2][2] = {self.RECOVERABILITY}
        objectives[0][0][2][3] = {self.MISSION_CONTINUITY}
        
        # Layer 3: APPL
        objectives[0][0][3][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][0][3][1] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][0][3][2] = {self.RECOVERABILITY}
        objectives[0][0][3][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        # Component 1: LAN
        # Layer 0: HW
        objectives[0][1][0][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][1][0][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][1][0][2] = {self.RECOVERABILITY}
        objectives[0][1][0][3] = {self.MISSION_CONTINUITY}
        
        # Layer 1: FW
        objectives[0][1][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][1][1][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][1][1][2] = {self.RECOVERABILITY}
        objectives[0][1][1][3] = {self.MISSION_CONTINUITY}
        
        # Layer 2: NETW
        objectives[0][1][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][1][2][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][1][2][2] = {self.RECOVERABILITY}
        objectives[0][1][2][3] = {self.MISSION_CONTINUITY}
        
        # Layer 3: APPL
        objectives[0][1][3][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][1][3][1] = {self.INTEGRITY}
        objectives[0][1][3][2] = {self.RECOVERABILITY}
        objectives[0][1][3][3] = {self.MISSION_CONTINUITY}
        
        # Component 2: OT-sensor
        # Layer 0: HW
        objectives[0][2][0][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][0][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[0][2][0][2] = {self.RECOVERABILITY}
        objectives[0][2][0][3] = {self.MISSION_CONTINUITY}
        
        # Layer 1: FW
        objectives[0][2][1][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][1][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[0][2][1][2] = {self.RECOVERABILITY}
        objectives[0][2][1][3] = {self.MISSION_CONTINUITY}
        
        # Layer 2: NETW
        objectives[0][2][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][2][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[0][2][2][2] = {self.RECOVERABILITY}
        objectives[0][2][2][3] = {self.MISSION_CONTINUITY}
        
        # Layer 3: APPL
        objectives[0][2][3][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][3][1] = {self.AVAILABILITY}
        objectives[0][2][3][2] = {self.RECOVERABILITY}
        objectives[0][2][3][3] = {self.MISSION_CONTINUITY}
        
        return objectives[0]

    """  Expert 2 objectives: Balanced approach emphasizing all objectives equally. """
    def _create_expert2_objectives(self):
        objectives = [[[set() for _ in range(4)] for _ in range(4)] for _ in range(3)]
        
        # Component 0: OT-control
        objectives[0][0][0] = {self.AVAILABILITY, self.INTEGRITY}
        objectives[0][0][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][0][2] = {self.RECOVERABILITY, self.AVAILABILITY}
        objectives[0][0][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        objectives[0][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][1][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][1][2] = {self.RECOVERABILITY}
        objectives[0][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][2][2] = {self.RECOVERABILITY}
        objectives[0][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][3][0] = {self.INTEGRITY}
        objectives[0][3][1] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][3][2] = {self.RECOVERABILITY}
        objectives[0][3][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        # Component 1: LAN
        objectives[1][0][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[1][0][1] = {self.SURVIVABILITY}
        objectives[1][0][2] = {self.RECOVERABILITY}
        objectives[1][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[1][1][1] = {self.SURVIVABILITY}
        objectives[1][1][2] = {self.RECOVERABILITY}
        objectives[1][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[1][2][1] = {self.SURVIVABILITY}
        objectives[1][2][2] = {self.RECOVERABILITY}
        objectives[1][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][3][0] = {self.INTEGRITY}
        objectives[1][3][1] = {self.INTEGRITY}
        objectives[1][3][2] = {self.RECOVERABILITY}
        objectives[1][3][3] = {self.MISSION_CONTINUITY}
        
        # Component 2: OT-sensor
        objectives[2][0][0] = {self.AVAILABILITY}
        objectives[2][0][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][0][2] = {self.RECOVERABILITY}
        objectives[2][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][1][0] = {self.AVAILABILITY}
        objectives[2][1][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][1][2] = {self.RECOVERABILITY}
        objectives[2][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[2][2][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][2][2] = {self.RECOVERABILITY}
        objectives[2][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][3][0] = {self.AVAILABILITY}
        objectives[2][3][1] = {self.AVAILABILITY}
        objectives[2][3][2] = {self.RECOVERABILITY}
        objectives[2][3][3] = {self.MISSION_CONTINUITY}
        
        return objectives

    """  Expert 3 objectives: Focus on recovery and adaptation.
    Emphasizes recoverability, degraded_operation, and mission_continuity.  """
    def _create_expert3_objectives(self):
        objectives = [[[set() for _ in range(4)] for _ in range(4)] for _ in range(3)]
        
        # Component 0: OT-control
        objectives[0][0][0] = {self.AVAILABILITY}
        objectives[0][0][1] = {self.SURVIVABILITY}
        objectives[0][0][2] = {self.RECOVERABILITY, self.DEGRADED_OPERATION}
        objectives[0][0][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        objectives[0][1][0] = {self.INTEGRITY}
        objectives[0][1][1] = {self.SURVIVABILITY}
        objectives[0][1][2] = {self.RECOVERABILITY, self.DEGRADED_OPERATION}
        objectives[0][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][2][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][1] = {self.SURVIVABILITY}
        objectives[0][2][2] = {self.RECOVERABILITY, self.DEGRADED_OPERATION}
        objectives[0][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][3][0] = {self.INTEGRITY}
        objectives[0][3][1] = {self.INTEGRITY}
        objectives[0][3][2] = {self.RECOVERABILITY, self.DEGRADED_OPERATION}
        objectives[0][3][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        # Component 1: LAN
        objectives[1][0][0] = {self.AVAILABILITY}
        objectives[1][0][1] = {self.SURVIVABILITY}
        objectives[1][0][2] = {self.RECOVERABILITY}
        objectives[1][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][1][0] = {self.INTEGRITY}
        objectives[1][1][1] = {self.SURVIVABILITY}
        objectives[1][1][2] = {self.RECOVERABILITY}
        objectives[1][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][2][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[1][2][1] = {self.SURVIVABILITY}
        objectives[1][2][2] = {self.RECOVERABILITY}
        objectives[1][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][3][0] = {self.INTEGRITY}
        objectives[1][3][1] = {self.INTEGRITY}
        objectives[1][3][2] = {self.RECOVERABILITY}
        objectives[1][3][3] = {self.MISSION_CONTINUITY}
        
        # Component 2: OT-sensor
        objectives[2][0][0] = {self.AVAILABILITY}
        objectives[2][0][1] = {self.SURVIVABILITY}
        objectives[2][0][2] = {self.RECOVERABILITY}
        objectives[2][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][1][0] = {self.AVAILABILITY}
        objectives[2][1][1] = {self.SURVIVABILITY}
        objectives[2][1][2] = {self.RECOVERABILITY}
        objectives[2][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][2][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[2][2][1] = {self.SURVIVABILITY}
        objectives[2][2][2] = {self.RECOVERABILITY}
        objectives[2][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][3][0] = {self.AVAILABILITY}
        objectives[2][3][1] = {self.AVAILABILITY}
        objectives[2][3][2] = {self.RECOVERABILITY}
        objectives[2][3][3] = {self.MISSION_CONTINUITY}
        
        return objectives

    """  Expert 4 objectives: Focus on robustness and withstanding.
    Emphasizes survivability and all security objectives.  """
    def _create_expert4_objectives(self):
        objectives = [[[set() for _ in range(4)] for _ in range(4)] for _ in range(3)]
        
        # Component 0: OT-control
        objectives[0][0][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][0][1] = {self.INTEGRITY, self.SURVIVABILITY, self.AVAILABILITY}
        objectives[0][0][2] = {self.RECOVERABILITY}
        objectives[0][0][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        objectives[0][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][1][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][1][2] = {self.RECOVERABILITY}
        objectives[0][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[0][2][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[0][2][2] = {self.RECOVERABILITY}
        objectives[0][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[0][3][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[0][3][1] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[0][3][2] = {self.RECOVERABILITY}
        objectives[0][3][3] = {self.MISSION_CONTINUITY, self.DEGRADED_OPERATION}
        
        # Component 1: LAN
        objectives[1][0][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[1][0][1] = {self.SURVIVABILITY}
        objectives[1][0][2] = {self.RECOVERABILITY}
        objectives[1][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][1][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[1][1][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[1][1][2] = {self.RECOVERABILITY}
        objectives[1][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[1][2][1] = {self.INTEGRITY, self.SURVIVABILITY}
        objectives[1][2][2] = {self.RECOVERABILITY}
        objectives[1][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[1][3][0] = {self.CONFIDENTIALITY, self.INTEGRITY}
        objectives[1][3][1] = {self.INTEGRITY}
        objectives[1][3][2] = {self.RECOVERABILITY}
        objectives[1][3][3] = {self.MISSION_CONTINUITY}
        
        # Component 2: OT-sensor
        objectives[2][0][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[2][0][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][0][2] = {self.RECOVERABILITY}
        objectives[2][0][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][1][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[2][1][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][1][2] = {self.RECOVERABILITY}
        objectives[2][1][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][2][0] = {self.CONFIDENTIALITY, self.INTEGRITY, self.AVAILABILITY}
        objectives[2][2][1] = {self.AVAILABILITY, self.SURVIVABILITY}
        objectives[2][2][2] = {self.RECOVERABILITY}
        objectives[2][2][3] = {self.MISSION_CONTINUITY}
        
        objectives[2][3][0] = {self.INTEGRITY, self.AVAILABILITY}
        objectives[2][3][1] = {self.AVAILABILITY}
        objectives[2][3][2] = {self.RECOVERABILITY}
        objectives[2][3][3] = {self.MISSION_CONTINUITY}
        
        return objectives

    def get_reconciled_objectives_matrix(self, consensus_threshold=0.5):
        """Return consensus objective sets for each component/layer/goal.

        An objective is retained only when its assessor support fraction is
        greater than the threshold. At the default 0.5 threshold, strict
        majority is required, so a 2-2 tie is excluded.
        """
        if not 0 <= consensus_threshold <= 1:
            raise ValueError("Consensus threshold must be between 0 and 1")
        if not self.all_objectives:
            raise ValueError("At least one assessor is required")

        assessor_count = len(self.all_objectives)
        reconciled = [
            [[set() for _ in range(4)] for _ in range(4)]
            for _ in range(3)
        ]
        for component_index in range(3):
            for layer_index in range(4):
                for goal_index in range(4):
                    for objective in self.ALL_OBJECTIVES:
                        support = sum(
                            objective in assessor_matrix[component_index][layer_index][goal_index]
                            for assessor_matrix in self.all_objectives
                        ) / assessor_count
                        if support > consensus_threshold:
                            reconciled[component_index][layer_index][goal_index].add(objective)

        return reconciled

    #Return one 0..1 objective-coverage score per component/layer/goal."""
    def get_normalized_objectives_matrix(self, consensus_threshold=0.5):
        reconciled = self.get_reconciled_objectives_matrix(consensus_threshold)
        objective_count = len(self.ALL_OBJECTIVES)
        return np.array(
            [
                [
                    [len(objective_set) / objective_count for objective_set in layer]
                    for layer in component
                ]
                for component in reconciled
            ],
            dtype=float,
        )

    def print_reconciled_objectives_matrix(self, consensus_threshold=0.5):
        """Print consensus objective sets by component, layer, and goal."""
        component_names = ["OT-control", "LAN", "OT-sensor"]
        layer_names = ["HW", "FW", "NETW", "APPL"]
        goal_names = ["ANT", "WITH", "REC", "ADPT"]
        reconciled = self.get_reconciled_objectives_matrix(consensus_threshold)

        print("\nReconciled Resilience Objectives")
        for component_index, component_name in enumerate(component_names):
            print(f"\n{component_name}")
            for layer_index, layer_name in enumerate(layer_names):
                print(f"  {layer_name}:")
                for goal_index, goal_name in enumerate(goal_names):
                    objective_set = reconciled[component_index][layer_index][goal_index]
                    value = ", ".join(sorted(objective_set)) if objective_set else "none"
                    print(f"    {goal_name:<5} {value}")

    def print_normalized_objectives_with_scores(self, consensus_threshold=0.5):
        """Print normalized objective coverage by component, layer, and goal."""
        component_names = ["OT-control", "LAN", "OT-sensor"]
        layer_names = ["HW", "FW", "NETW", "APPL"]
        goal_names = ["ANT", "WITH", "REC", "ADPT"]
        scores = self.get_normalized_objectives_matrix(consensus_threshold)

        print("\nNormalized Resilience Objective Coverage")
        print("=" * 78)
        for component_index, component_name in enumerate(component_names):
            print(f"\n{component_name}")
            print(f"{'Layer':<10} | " + " | ".join(f"{goal:>6}" for goal in goal_names))
            print("-" * 53)
            for layer_index, layer_name in enumerate(layer_names):
                values = scores[component_index, layer_index]
                print(
                    f"{layer_name:<10} | "
                    + " | ".join(f"{value:6.2f}" for value in values)
                )



