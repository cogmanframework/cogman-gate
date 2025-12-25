"""
Perception Module Usage Examples

Demonstrates usage of Decoder, Energy Estimator, and Phrase Extractor
"""

import sys
import os
import numpy as np

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from perception import Decoder, DecodeResult, TrustLevel
from perception import EnergyEstimator, IPSHState
from perception import PhraseExtractor, PEU


def example_decoder():
    """Example: Decoder usage"""
    print("=== Decoder Example ===")
    
    # Create decoder
    decoder = Decoder(verify_signature=False)
    
    # Register a device
    decoder.register_device("device_001", {"type": "sensor", "location": "room1"})
    
    # Create test packet
    packet = {
        "device_id": "device_001",
        "seq": 1,
        "ts": 1234567890.0,
        "mode": "features",
        "phi": [0.5, 0.3, 0.8, 0.2, 0.6],
        "meta": {
            "fps": 30.0,
            "sensor": "camera"
        }
    }
    
    # Decode packet
    result = decoder.decode(packet)
    
    print(f"Device ID: {result.device_id}")
    print(f"Sequence: {result.sequence}")
    print(f"OK: {result.ok}")
    print(f"Trust Level: {result.trust_level}")
    print(f"Data: {result.x_t}")
    print()


def example_energy_estimator():
    """Example: Energy Estimator usage"""
    print("=== Energy Estimator Example ===")
    
    # Create estimator
    estimator = EnergyEstimator(mu_I=0.5, sigma_I=0.3, lambda_stability=1.0)
    
    # Current feature vector
    phi_t = np.array([0.8, 0.6, 0.4, 0.9, 0.3])
    
    # Previous feature vector (optional)
    phi_prev = np.array([0.7, 0.5, 0.3, 0.8, 0.2])
    
    # Estimate IPSH state
    state = estimator.estimate(phi_t, phi_prev)
    
    print(f"Intensity (I): {state.I:.3f}")
    print(f"Polarity (P): {state.P:.3f}")
    print(f"Stability (S): {state.S:.3f}")
    print(f"Entropy (H): {state.H:.3f}")
    print(f"Decision Energy (dE): {state.dE:.3f}")
    print()


def example_phrase_extractor():
    """Example: Phrase Extractor usage"""
    print("=== Phrase Extractor Example ===")
    
    # Create extractor
    extractor = PhraseExtractor(
        energy_threshold=0.1,
        max_phrase_length=10,
        language="auto"
    )
    
    # Test text (English)
    text_en = "I want to create a great system that works well and makes users happy."
    
    print(f"Text: {text_en}")
    print()
    
    # Extract phrases
    peu_list = extractor.extract(text_en)
    
    print(f"Extracted {len(peu_list)} phrases:")
    for i, peu in enumerate(peu_list, 1):
        print(f"\n{i}. Phrase: '{peu.phrase}'")
        print(f"   Role: {peu.role}")
        print(f"   I={peu.I:.3f}, P={peu.P:.3f}, S={peu.S:.3f}, H={peu.H:.3f}")
        print(f"   Phase={peu.phase:.3f}, Freq={peu.freq:.1f} Hz")
        print(f"   Energy={peu.energy:.3f}, Confidence={peu.confidence:.3f}")
    
    print()
    
    # Test text (Thai)
    text_th = "ฉันต้องการสร้างระบบที่ดีมากและใช้งานง่าย"
    
    print(f"Text (Thai): {text_th}")
    print()
    
    peu_list_th = extractor.extract(text_th)
    
    print(f"Extracted {len(peu_list_th)} phrases:")
    for i, peu in enumerate(peu_list_th, 1):
        print(f"\n{i}. Phrase: '{peu.phrase}'")
        print(f"   Role: {peu.role}")
        print(f"   I={peu.I:.3f}, P={peu.P:.3f}, S={peu.S:.3f}, H={peu.H:.3f}")
        print(f"   Energy={peu.energy:.3f}")
    print()


def example_integration():
    """Example: Integration of all modules"""
    print("=== Integration Example ===")
    
    # 1. Decode packet
    decoder = Decoder()
    decoder.register_device("sensor_01", {})
    
    packet = {
        "device_id": "sensor_01",
        "seq": 1,
        "ts": 1234567890.0,
        "mode": "features",
        "phi": [0.8, 0.6, 0.4, 0.9, 0.3],
        "meta": {}
    }
    
    decode_result = decoder.decode(packet)
    
    if decode_result.ok and decode_result.trust_level == TrustLevel.OK:
        # 2. Estimate energy from features
        estimator = EnergyEstimator()
        phi_t = np.array(decode_result.x_t)
        ipsh_state = estimator.estimate(phi_t)
        
        print(f"Decoded packet: OK")
        print(f"IPSH State: I={ipsh_state.I:.3f}, P={ipsh_state.P:.3f}, "
              f"S={ipsh_state.S:.3f}, H={ipsh_state.H:.3f}")
        print(f"Decision Energy: {ipsh_state.dE:.3f}")
    
    # 3. Extract phrases from text
    extractor = PhraseExtractor()
    text = "I want to build a system that works well"
    peu_list = extractor.extract(text)
    
    print(f"\nExtracted {len(peu_list)} phrases from text")
    for peu in peu_list:
        print(f"  - '{peu.phrase}' (role={peu.role}, energy={peu.energy:.3f})")
    
    print()


if __name__ == "__main__":
    try:
        example_decoder()
        example_energy_estimator()
        example_phrase_extractor()
        example_integration()
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

