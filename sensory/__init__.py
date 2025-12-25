"""
Sensory Adapters (NO FORMULA)

Purpose: Receive input, extract features, NO interpretation
"""

from .base_adapter import SensorAdapter
from .text_adapter import TextAdapter
# Note: ImageAdapter and AudioAdapter are placeholders and not used in runtime
# Uncomment when implementing:
# from .image_adapter import ImageAdapter
# from .audio_adapter import AudioAdapter

__all__ = [
    'SensorAdapter',
    'TextAdapter',
    # 'ImageAdapter',  # Placeholder: Not implemented yet
    # 'AudioAdapter',  # Placeholder: Not implemented yet
]

