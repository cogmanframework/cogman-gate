"""
Energetic Perception (NO RAW)

Purpose: Uses EPS-8 result, builds trajectory
"""

from .perception_state import PerceptionState
from .trajectory_builder import TrajectoryBuilder, Trace, Trajectory, TraceManager
# Note: Resonance is implemented in memory/ fields, not here
# Note: ContextModulation is implemented in runtime/wm_controller.py, not here
from .decoder import Decoder, DecodeResult, TrustLevel
from .energy_estimator import EnergyEstimator, IPSHState
from .phrase_extractor import PhraseExtractor, PEU

__all__ = [
    'PerceptionState',
    'TrajectoryBuilder',
    'Trace',
    'Trajectory',
    'TraceManager',
    # 'Resonance',  # Removed: Not used, resonance is in memory/ fields
    # 'ContextModulation',  # Removed: Not used, context modulation is in runtime/wm_controller.py
    'Decoder',
    'DecodeResult',
    'TrustLevel',
    'EnergyEstimator',
    'IPSHState',
    'PhraseExtractor',
    'PEU',
]

