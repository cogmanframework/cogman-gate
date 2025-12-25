"""
Normalization (scaling / unit alignment only)

Purpose: Normalize features, NO formulas
"""

from typing import Dict, Any


def normalize_features(features: Dict[str, Any], bounds: Dict[str, tuple]) -> Dict[str, float]:
    """
    Normalize features to [0, 1] range.
    
    Args:
        features: Raw feature values
        bounds: Min/max bounds for each feature
    
    Returns:
        Normalized features in [0, 1] range
    """
    normalized = {}
    
    for key, value in features.items():
        if key in bounds:
            min_val, max_val = bounds[key]
            if max_val > min_val:
                normalized[key] = (value - min_val) / (max_val - min_val)
            else:
                normalized[key] = 0.0
        else:
            normalized[key] = float(value) if isinstance(value, (int, float)) else 0.0
    
    return normalized

