"""
Base Sensor Adapter (abstract SensorAdapter)

Purpose: Abstract base class for all sensor adapters
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class SensorAdapter(ABC):
    """
    Abstract base class for sensor adapters.
    
    Responsibility:
    - Receive raw input
    - Extract features
    - NO interpretation
    - NO formulas
    """
    
    @abstractmethod
    def process(self, raw_input: Any) -> Dict[str, Any]:
        """
        Process raw input and extract features.
        
        Returns:
            Dict with keys:
            - modality: str (e.g., "text", "image", "audio")
            - features: Dict[str, Any]
            - timestamp: float
            - source_id: str
        """
        pass
    
    @abstractmethod
    def validate(self, raw_input: Any) -> bool:
        """
        Validate raw input.
        
        Returns:
            True if valid, False otherwise
        """
        pass

