"""Derive normalized resilience-class intervals from four expert judgments."""

from math import isfinite

import numpy as np

if __package__:
    from . import ahpEstimator, sensitivityAnalysis
    from .configuration import configuration, parameters
else:
    import ahpEstimator
    import sensitivityAnalysis
    from configuration import configuration, parameters


class SaatyResilienceClassifier:
    #Build L1, L2, L3, and L4 intervals using group AHP.

    def __init__(self, expert_reference_values=None, sensitivity=0.05):
        self.build_intervals(expert_reference_values, sensitivity)

    def build_intervals(self, expert_reference_values=None, sensitivity = 0.05):
        if not isinstance(sensitivity, (int, float)) or not isfinite(sensitivity) or sensitivity < 0:
            raise ValueError("sensitivity must be a finite non-negative number")
        if expert_reference_values is None:
            expert_reference_values = configuration.DEFAULT_EXPERT_REFERENCE_VALUES

        references = np.asarray(expert_reference_values, dtype=float)
        if references.shape != (4, 4):
            raise ValueError("expert_reference_values must have shape (4, 4)")
        if not np.isfinite(references).all() or (references <= 0).any():
            raise ValueError("expert reference values must be finite and positive")
        if (np.diff(references, axis=1) <= 0).any():
            raise ValueError("each expert's values must increase from L1 through L4")

        self.expert_reference_values = references.copy()
        self.expert_matrices = np.stack([
            ahpEstimator.AHP.comparison_matrix_from_values(values)
            for values in references
        ])
        self.group_matrix = ahpEstimator.AHP.aggregate_matrices(self.expert_matrices)
        self.group_priorities, self.consistency_ratio = ahpEstimator.AHP.analyze_group(
            self.group_matrix
        )

        normalized = self.group_priorities / self.group_priorities[-1]
        if (np.diff(normalized) <= 0).any():
            raise ValueError("AHP priorities do not preserve the required class order")

        self.reference_points = dict(zip(parameters.LEVELS, normalized.tolist()))
        points = normalized.tolist()
        self.boundaries = tuple(
            (points[index] + points[index + 1]) / 2
            for index in range(len(points) - 1)
        )
        self.intervals = {
            level: (
                0.0 if index == 0 else self.boundaries[index - 1],
                1.0 if index == len(parameters.LEVELS) - 1 else self.boundaries[index],
            )
            for index, level in enumerate(parameters.LEVELS)
        }
        self.sensitivity_results = self._analyze_normalized_sensitivity(
            normalized, sensitivity
        )
        return self.sensitivity_results

    @staticmethod
    def _analyze_normalized_sensitivity(normalized, sensitivity):
        baseline_boundaries = tuple(
            (normalized[index] + normalized[index + 1]) / 2
            for index in range(len(normalized) - 1)
        )
        results = {}
        for index, level in enumerate(parameters.LEVELS):
            perturbed, redistribution_ratio = sensitivityAnalysis.increaseweights(
                normalized.tolist(), index, sensitivity
            )
            perturbed = np.asarray(perturbed, dtype=float)
            perturbed /= perturbed[-1]
            if (np.diff(perturbed) <= 0).any():
                raise ValueError(
                    f"sensitivity perturbation for {level} changes the class order"
                )

            boundaries = tuple(
                (perturbed[point] + perturbed[point + 1]) / 2
                for point in range(len(perturbed) - 1)
            )
            results[level] = {
                "redistribution_ratio": redistribution_ratio,
                "reference_points": dict(zip(parameters.LEVELS, perturbed.tolist())),
                "boundaries": boundaries,
                "boundary_deltas": tuple(
                    changed - baseline
                    for changed, baseline in zip(boundaries, baseline_boundaries)
                ),
            }
        return results

    # Return the level containing a finite normalized value in [0, 1].
    # This represent the civilian security level 
    def classify(self, value):
        if not isinstance(value, (int, float, np.number)) or not isfinite(value):
            raise ValueError("value must be a finite number between 0 and 1")
        if not 0 <= value <= 1:
            raise ValueError("value must be a finite number between 0 and 1")
        class_index = int(np.searchsorted(self.boundaries, value, side="right"))
        return parameters.LEVELS[class_index]