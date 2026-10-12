import numpy as np

if __package__:
    from .configuration.parameters import Goals, Layers
else:
    from configuration.parameters import Goals, Layers

# Container for resilience weight matrices.
# The weights follow the structure: [component_type, layer, goal]
# Component types: 1 (OT-control), 2 (LAN), 3 (OT-sensor)
# Layers: 4 (HW, FW, NETW, APPL)
# Goals: 4 (ANT, WITH, REC, ADPT)
#Contains 4 weight matrices representing opinions from 4 different experts.
class ResilienceWeights:
    
    def __init__(self):
        """Initialize weight matrices for 4 experts."""
        self.weights_expert1 = self._create_expert1_weights()
        self.weights_expert2 = self._create_expert2_weights()
        self.weights_expert3 = self._create_expert3_weights()
        self.weights_expert4 = self._create_expert4_weights()
        
        self.all_weights = [
            self.weights_expert1,
            self.weights_expert2,
            self.weights_expert3,
            self.weights_expert4
        ]

    # Expert 1 weights: Emphasizes network layer security and anticipation goals.
    # Focus on preventive measures and network protection.
    #Each row sums to 1.0 (normalized across goals).
    def _create_expert1_weights(self):
        weights = np.zeros((3, 4, 4), dtype=float)
        
        # Component 1: OT-control
        # Layer indices: 0=HW, 1=FW, 2=NETW, 3=APPL
        # Goal indices: 0=ANT, 1=WITH, 2=REC, 3=ADPT
        weights[0, 0, :] = [0.40, 0.35, 0.15, 0.10]  # HW layer
        weights[0, 1, :] = [0.45, 0.35, 0.15, 0.05]  # FW layer
        weights[0, 2, :] = [0.50, 0.30, 0.12, 0.08]  # NETW layer (emphasized)
        weights[0, 3, :] = [0.42, 0.30, 0.18, 0.10]  # APPL layer
        
        # Component 2: LAN
        weights[1, 0, :] = [0.38, 0.32, 0.20, 0.10]  # HW layer
        weights[1, 1, :] = [0.42, 0.33, 0.17, 0.08]  # FW layer
        weights[1, 2, :] = [0.48, 0.28, 0.15, 0.09]  # NETW layer (emphasized)
        weights[1, 3, :] = [0.40, 0.30, 0.20, 0.10]  # APPL layer
        
        # Component 3: OT-sensor
        weights[2, 0, :] = [0.36, 0.34, 0.20, 0.10]  # HW layer
        weights[2, 1, :] = [0.40, 0.34, 0.18, 0.08]  # FW layer
        weights[2, 2, :] = [0.46, 0.30, 0.16, 0.08]  # NETW layer (emphasized)
        weights[2, 3, :] = [0.38, 0.32, 0.20, 0.10]  # APPL layer
        
        return weights
    
    def _create_expert2_weights(self):
        """
        Expert 2 weights: Balanced approach across all layers and goals.
        Equal distribution across anticipation, withstanding, recovery, and adaptation.
        Each row sums to 1.0 (normalized across goals).
        """
        weights = np.zeros((3, 4, 4), dtype=float)
        
        # Component 1: OT-control
        weights[0, 0, :] = [0.25, 0.25, 0.25, 0.25]  # HW layer (balanced)
        weights[0, 1, :] = [0.25, 0.25, 0.25, 0.25]  # FW layer (balanced)
        weights[0, 2, :] = [0.25, 0.25, 0.25, 0.25]  # NETW layer (balanced)
        weights[0, 3, :] = [0.25, 0.25, 0.25, 0.25]  # APPL layer (balanced)
        
        # Component 2: LAN
        weights[1, 0, :] = [0.25, 0.25, 0.25, 0.25]  # HW layer (balanced)
        weights[1, 1, :] = [0.25, 0.25, 0.25, 0.25]  # FW layer (balanced)
        weights[1, 2, :] = [0.25, 0.25, 0.25, 0.25]  # NETW layer (balanced)
        weights[1, 3, :] = [0.25, 0.25, 0.25, 0.25]  # APPL layer (balanced)
        
        # Component 3: OT-sensor
        weights[2, 0, :] = [0.25, 0.25, 0.25, 0.25]  # HW layer (balanced)
        weights[2, 1, :] = [0.25, 0.25, 0.25, 0.25]  # FW layer (balanced)
        weights[2, 2, :] = [0.25, 0.25, 0.25, 0.25]  # NETW layer (balanced)
        weights[2, 3, :] = [0.25, 0.25, 0.25, 0.25]  # APPL layer (balanced)
        
        return weights
    
    def _create_expert3_weights(self):
        """
        Expert 3 weights: Emphasizes recovery and adaptation capabilities.
        Focus on post-incident response and system adaptability.
        Each row sums to 1.0 (normalized across goals).
        """
        weights = np.zeros((3, 4, 4), dtype=float)
        
        # Component 1: OT-control
        weights[0, 0, :] = [0.10, 0.15, 0.30, 0.45]  # HW layer (recovery/adaptation emphasized)
        weights[0, 1, :] = [0.08, 0.14, 0.28, 0.50]  # FW layer (recovery/adaptation emphasized)
        weights[0, 2, :] = [0.06, 0.12, 0.26, 0.56]  # NETW layer (recovery/adaptation emphasized)
        weights[0, 3, :] = [0.08, 0.14, 0.28, 0.50]  # APPL layer (recovery/adaptation emphasized)
        
        # Component 2: LAN
        weights[1, 0, :] = [0.12, 0.18, 0.32, 0.38]  # HW layer
        weights[1, 1, :] = [0.10, 0.16, 0.30, 0.44]  # FW layer
        weights[1, 2, :] = [0.08, 0.14, 0.28, 0.50]  # NETW layer (recovery/adaptation emphasized)
        weights[1, 3, :] = [0.10, 0.16, 0.30, 0.44]  # APPL layer
        
        # Component 3: OT-sensor
        weights[2, 0, :] = [0.14, 0.20, 0.34, 0.32]  # HW layer
        weights[2, 1, :] = [0.12, 0.18, 0.32, 0.38]  # FW layer
        weights[2, 2, :] = [0.10, 0.16, 0.30, 0.44]  # NETW layer (recovery/adaptation emphasized)
        weights[2, 3, :] = [0.12, 0.18, 0.32, 0.38]  # APPL layer
        
        return weights
    
    def _create_expert4_weights(self):
        """
        Expert 4 weights: Emphasizes withstanding (resistance) capabilities.
        Each row sums to 1.0 (normalized across goals).
        """
        weights = np.zeros((3, 4, 4), dtype=float)
        
        # Component 1: OT-control
        weights[0, 0, :] = [0.12, 0.55, 0.20, 0.13]  # HW layer (withstanding emphasized)
        weights[0, 1, :] = [0.10, 0.60, 0.18, 0.12]  # FW layer (withstanding emphasized)
        weights[0, 2, :] = [0.08, 0.62, 0.16, 0.14]  # NETW layer (withstanding emphasized)
        weights[0, 3, :] = [0.10, 0.54, 0.22, 0.14]  # APPL layer (withstanding emphasized)
        
        # Component 2: LAN
        weights[1, 0, :] = [0.14, 0.52, 0.22, 0.12]  # HW layer
        weights[1, 1, :] = [0.12, 0.58, 0.20, 0.10]  # FW layer
        weights[1, 2, :] = [0.10, 0.60, 0.18, 0.12]  # NETW layer (withstanding emphasized)
        weights[1, 3, :] = [0.12, 0.52, 0.24, 0.12]  # APPL layer
        
        # Component 3: OT-sensor
        weights[2, 0, :] = [0.16, 0.50, 0.24, 0.10]  # HW layer
        weights[2, 1, :] = [0.14, 0.56, 0.22, 0.08]  # FW layer
        weights[2, 2, :] = [0.14, 0.50, 0.26, 0.10]  # NETW layer (withstanding emphasized)
        weights[2, 3, :] = np.array([0.60, 0.65, 0.55, 0.50]) / 2.30  # APPL layer
        
        return weights

    # Get weight matrix for a specific expert.
    # input: expert_number (int): Expert number (1-4)
    # returns: np.ndarray: Weight matrix of shape (3, 4, 4)
    def get_weights_for_expert(self, expert_number):
        if expert_number < 1 or expert_number > 4:
            raise ValueError(f"Expert number must be between 1 and 4, got {expert_number}")
        return self.all_weights[expert_number - 1]

    #Get all weight matrices.
    #returns: list: List of 4 weight matrices
    def get_all_weights(self):
        return self.all_weights

    # Get average weights across all experts interviewed for the purpose.
    # returns:  np.ndarray: Average weight matrix of shape (3, 4, 4): 3 components, 4 goals and 4 layers """
    def get_average_weights(self, oppinion_specialists):
        return np.average(self.all_weights, axis=0, weights=oppinion_specialists)
    
    def print_weights_summary(self):
        """Print a summary of weights for each expert and component type."""
        component_names = {0: "OT-control", 1: "LAN", 2: "OT-sensor"}
        layer_names = ["HW", "FW", "NETW", "APPL"]
        goal_names = ["ANT", "WITH", "REC", "ADPT"]
        
        for expert_idx, weights in enumerate(self.all_weights, 1):
            print(f"\n{'='*60}")
            print(f"Expert {expert_idx} - Weights Summary")
            print(f"{'='*60}")
            for comp_idx in range(3):
                print(f"\n{component_names[comp_idx]}:")
                print(f"{'Layer':<10} | {' | '.join(f'{g:>6}' for g in goal_names)}")
                print(f"{'-'*10}-+-{'-'*31}")
                for layer_idx, layer_name in enumerate(layer_names):
                    values = weights[comp_idx, layer_idx, :]
                    print(f"{layer_name:<10} | {' | '.join(f'{v:>6.2f}' for v in values)}")


if __name__ == "__main__":
    # Example usage
    weights = ResilienceWeights()
    weights.print_weights_summary()
    
    print(f"\n{'='*60}")
    print("Average Weights Across All Experts")
    print(f"{'='*60}")
    oppinion_specialists = [0.4, 0.3, 0.2, 0.1]
    avg_weights = weights.get_average_weights(oppinion_specialists)
    
    component_names = {0: "OT-control", 1: "LAN", 2: "OT-sensor"}
    layer_names = ["HW", "FW", "NETW", "APPL"]
    goal_names = ["ANT", "WITH", "REC", "ADPT"]
    
    for comp_idx in range(3):
        print(f"\n{component_names[comp_idx]}:")
        print(f"{'Layer':<10} | {' | '.join(f'{g:>6}' for g in goal_names)}")
        print(f"{'-'*10}-+-{'-'*31}")
        for layer_idx, layer_name in enumerate(layer_names):
            values = avg_weights[comp_idx, layer_idx, :]
            print(f"{layer_name:<10} | {' | '.join(f'{v:>6.2f}' for v in values)}")
