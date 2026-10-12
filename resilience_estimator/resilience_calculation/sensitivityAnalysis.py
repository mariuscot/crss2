# in vector <weights> the component at <index> is modified by <imcrement> factor
# increment has to be less than 1 to match the scaling of the weights
# sum of weights has to be 1 (nornalized) 
def increaseweights(weights, index, increment):
    if not 0 <= index < len(weights):
        raise IndexError("weight index is outside the vector")
    if increment < 0:
        raise ValueError("increment must be non-negative")

    other_weight_total = sum(
        weight for weight_index, weight in enumerate(weights) if weight_index != index
    )
    if other_weight_total <= 0 or increment > other_weight_total:
        raise ValueError("increment must be smaller than the other weights' total")

    total_weight = sum(weights)
    ratio = (total_weight - weights[index] - increment) / other_weight_total
    new_weights = [weight * ratio for weight in weights]
    new_weights[index] = weights[index] + increment
    return new_weights, ratio

