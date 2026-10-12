#expert_reference_values is ordered by expert, then by class in
#``LEVELS`` order, and must have shape (4, 4). 

# Elements to build the Security levels for civilian resilience classification using Saaty AHP.
DEFAULT_EXPERT_REFERENCE_VALUES = (
	(0.15, 0.40, 0.80, 1.00),
	(0.20, 0.45, 0.75, 1.00),
	(0.10, 0.50, 0.85, 1.00),
	(0.15, 0.40, 0.90, 1.00),
)

# Elements to build the propagation strength 
# layer coupling as first element, goal coupling as second element
LAYER_GOAL_COUPLING_STRENGTHS = {
	"OT-OT": (0.95, 0.85),
	"OT-IT": (1.0, 1.0),
	"IT-OT": (0.9, 1.0),
	"IT-IT": (0.85, 1.0),
}

# applicability as first eelment, containment as second element
APPLICABILITY_CONTAINMENT_TRANSITIONS = {
	"state": (1.0, 0.8),
	"data": (0.95, 0.8),
	"control": (1.0, 0.8),
	"actuation": (0.0, 0.8),
}

# Military resilience
# initial weights for building MMCM
MMCM_INITIAL_WEIGHTS = (0.4, 0.3, 0.4)

