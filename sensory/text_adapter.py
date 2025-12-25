"""
Text Adapter

Purpose: Process text input, extract features
"""

from .base_adapter import SensorAdapter
from typing import Dict, Any
import time


class TextAdapter(SensorAdapter):
    """
    Text sensor adapter.
    
    Responsibility:
    - Receive text input
    - Extract text features (length, tokens, etc.)
    - NO interpretation
    - NO formulas
    """
    
    def process(self, raw_input: str) -> Dict[str, Any]:
        """Process text input."""
        if not isinstance(raw_input, str):
            raise ValueError("Input must be a string")
        
        return {
            "modality": "text",
            "features": {
                "text": raw_input,
                "length": len(raw_input),
                "token_count": len(raw_input.split()),
            },
            "timestamp": time.time(),
            "source_id": "text_input",
        }
    
    def validate(self, raw_input: Any) -> bool:
        """Validate text input."""
        return isinstance(raw_input, str) and len(raw_input) > 0

