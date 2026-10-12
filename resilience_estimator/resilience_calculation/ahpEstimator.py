import numpy as np

class AHP:
    """AHP operations for Saaty comparison matrices and group judgments."""

    @staticmethod
    def reference_ratio_to_saaty(ratio):
        if ratio <= 0:
            raise ValueError("ratio must be positive")
        if ratio < 1:
            return 1 / AHP.reference_ratio_to_saaty(1 / ratio)
        if np.isclose(ratio, 3.5):
            return 3
        return min(9, max(1, int(np.floor(ratio + 0.5))))

    @classmethod
    def comparison_matrix_from_values(cls, values):
        values = np.asarray(values, dtype=float)
        if values.ndim != 1 or len(values) < 2:
            raise ValueError("values must be a one-dimensional sequence of at least two values")
        if not np.isfinite(values).all() or (values <= 0).any():
            raise ValueError("values must be finite and positive")

        matrix = np.ones((len(values), len(values)), dtype=float)
        for row in range(len(values)):
            for column in range(row + 1, len(values)):
                judgment = cls.reference_ratio_to_saaty(values[column] / values[row])
                matrix[row, column] = 1.0 / judgment
                matrix[column, row] = judgment
        return matrix

    @staticmethod
    def aggregate_matrices(matrices):
        matrices = np.asarray(matrices, dtype=float)
        if matrices.ndim != 3 or matrices.shape[1] != matrices.shape[2]:
            raise ValueError("matrices must have shape (experts, n, n)")
        if not np.isfinite(matrices).all() or (matrices <= 0).any():
            raise ValueError("matrix judgments must be finite and positive")
        return np.exp(np.mean(np.log(matrices), axis=0))

    @staticmethod
    def principal_eigenvector(matrix):
        matrix = np.asarray(matrix, dtype=float)
        if matrix.ndim != 2 or matrix.shape[0] != matrix.shape[1]:
            raise ValueError("matrix must be square")
        eigenvalues, eigenvectors = np.linalg.eig(matrix)
        principal_index = int(np.argmax(eigenvalues.real))
        priorities = eigenvectors[:, principal_index].real
        if priorities.sum() < 0:
            priorities = -priorities
        return priorities / priorities.sum()

    @staticmethod
    def consistency_ratio(matrix, priorities):
        return calculateCR(matrix, priorities)

    @classmethod
    def analyze_group(cls, matrix):
        priorities = cls.principal_eigenvector(matrix)
        return priorities, cls.consistency_ratio(matrix, priorities)


def get_saaty_scale():
    return [1, 2, 3, 4, 5, 6, 7, 8, 9]


def map_ratio_to_saaty(ratio):
    if ratio <= 0:
        raise ValueError("ratio must be positive")

    if ratio < 1:
        return 1 / map_ratio_to_saaty(1 / ratio)

    thresholds = [
        (1.2, 1),
        (1.5, 2),
        (2.0, 3),
        (3.0, 4),
        (5.0, 5),
        (7.0, 6),
        (9.0, 7),
    ]

    for limit, value in thresholds:
        if ratio < limit:
            return value

    return 9
    # Construct 2D layer_weights array: [layers][components * goals]
    # Shape: [4, 12] where 4 layers and 12 = 3 components * 4 goals
    layer_weights = np.zeros((4, 3 * 4), dtype=float)
    
    # Fill layer_weights by iterating through layers, components, and goals
    for layer_idx in range(4):
        for comp_idx in range(3):
            for goal_idx in range(4):
                # Flatten index: comp_idx * 4 + goal_idx
                flattened_idx = comp_idx * 4 + goal_idx
                layer_weights[layer_idx, flattened_idx] = expert_weights[comp_idx, layer_idx, goal_idx]
    
    return layer_weights

def conduct_ahp_analysis_layer(weights):
    n = len(weights)
    comparison_matrix = [[1 for _ in range(n)] for _ in range(n)]

    for i in range(n):
        for j in range(i + 1, n):
            ratio = weights[i] / weights[j]
            value = map_ratio_to_saaty(ratio)
            comparison_matrix[i][j] = value
            comparison_matrix[j][i] = 1 / value

    # Calculate the normalized weights
    column_sums = [sum(comparison_matrix[i][j] for i in range(n)) for j in range(n)]
    normalized_matrix = [[comparison_matrix[i][j] / column_sums[j] for j in range(n)] for i in range(n)]

    # Calculate the average of each row to get the final weights
    new_weights = [sum(normalized_matrix[i]) / n for i in range(n)]
    cr = calculateCR(comparison_matrix, new_weights)    
    return new_weights, cr

def conduct_ahp_analysis_component(weights):
    crArray = []
    estimatedWeightsArray = []
    for i in range(len(weights)):
        estimatedWeights, cr = conduct_ahp_analysis_layer(weights[i])
        estimatedWeightsArray.append(estimatedWeights)
        crArray.append(cr)
    return estimatedWeightsArray, crArray

def conduct_ahp_analysis_overall(weights):
    crArray = []
    estimatedWeightsArray = []
    for i in range(len(weights)):
        estimatedWeights, cr = conduct_ahp_analysis_component(weights[i])
        estimatedWeightsArray.append(estimatedWeights)
        crArray.append(cr)
    return estimatedWeightsArray, crArray

def calculateCR(comparison_matrix, new_weights):
    n = len(comparison_matrix)
    weighted_sum_vector = [sum(comparison_matrix[i][j] * new_weights[j] for j in range(n)) for i in range(n)]
    lambda_max = sum(weighted_sum_vector[i] / new_weights[i] for i in range(n)) / n
    CI = (lambda_max - n) / (n - 1)
    RI_dict = {1: 0.00, 2: 0.00, 3: 0.58, 4: 0.90, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45}
    RI = RI_dict.get(n, 1.49)  
    CR = CI / RI if RI != 0 else 0
    return CR

