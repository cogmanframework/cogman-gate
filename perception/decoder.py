"""
Decoder Module

Purpose: Decode and verify input packets
"""

from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import hashlib
import hmac


class TrustLevel(str, Enum):
    """Trust level for decoded packets"""
    OK = "OK"
    WARN = "WARN"
    FAIL = "FAIL"


@dataclass
class DecodeResult:
    """Result of packet decoding"""
    x_t: Any  # Raw data or features
    ok: bool  # Verification status
    meta: Dict[str, Any]  # Metadata
    device_id: str
    sequence: int
    timestamp: float
    trust_level: TrustLevel


class Decoder:
    """
    Decoder for input packets.
    
    Verifies device registration, sequence, signature, and extracts data.
    """
    
    def __init__(self, 
                 verify_signature: bool = False,
                 secret_key: Optional[str] = None,
                 max_sequence_gap: int = 1000):
        """
        Initialize decoder.
        
        Args:
            verify_signature: Enable signature verification
            secret_key: Secret key for signature verification
            max_sequence_gap: Maximum allowed sequence gap
        """
        self.verify_signature = verify_signature
        self.secret_key = secret_key
        self.max_sequence_gap = max_sequence_gap
        
        # Device registry (device_id -> last_sequence)
        self.device_registry: Dict[str, int] = {}
        
        # Registered devices (in production, load from database)
        self.registered_devices: Dict[str, Dict[str, Any]] = {}
    
    def register_device(self, device_id: str, device_info: Dict[str, Any]):
        """
        Register a device.
        
        Args:
            device_id: Device identifier
            device_info: Device information (public key, etc.)
        """
        self.registered_devices[device_id] = device_info
        if device_id not in self.device_registry:
            self.device_registry[device_id] = -1
    
    def decode(self, packet: Dict[str, Any]) -> DecodeResult:
        """
        Decode and verify packet.
        
        Args:
            packet: Input packet dictionary
        
        Returns:
            DecodeResult with decoded data and verification status
        """
        # Extract basic fields
        device_id = packet.get("device_id", "")
        sequence = packet.get("seq", -1)
        timestamp = packet.get("ts", 0.0)
        mode = packet.get("mode", "raw")
        meta = packet.get("meta", {})
        
        # Initialize result
        result = DecodeResult(
            x_t=None,
            ok=False,
            meta=meta,
            device_id=device_id,
            sequence=sequence,
            timestamp=timestamp,
            trust_level=TrustLevel.FAIL
        )
        
        # 1. Verify device registration
        if not self._verify_device_registration(device_id):
            result.trust_level = TrustLevel.FAIL
            return result
        
        # 2. Verify sequence (prevent replay)
        if not self._verify_sequence(device_id, sequence):
            result.trust_level = TrustLevel.WARN
            # Continue processing but mark as warning
        
        # 3. Verify signature (if enabled)
        if self.verify_signature:
            if not self._verify_signature(packet):
                result.trust_level = TrustLevel.FAIL
                return result
        
        # 4. Extract data based on mode
        if mode == "features":
            phi = packet.get("phi", [])
            if not phi:
                result.trust_level = TrustLevel.FAIL
                return result
            result.x_t = phi
        elif mode == "raw":
            raw = packet.get("raw")
            if raw is None:
                result.trust_level = TrustLevel.FAIL
                return result
            result.x_t = raw
        else:
            result.trust_level = TrustLevel.FAIL
            return result
        
        # 5. Verify hash (if provided)
        if "phi_hash" in packet:
            if not self._verify_hash(result.x_t, packet["phi_hash"]):
                result.trust_level = TrustLevel.WARN
                # Continue but mark as warning
        
        # 6. Update sequence tracker
        self.device_registry[device_id] = sequence
        
        # Set success
        result.ok = True
        if result.trust_level == TrustLevel.FAIL:
            result.trust_level = TrustLevel.OK
        
        return result
    
    def _verify_device_registration(self, device_id: str) -> bool:
        """Verify device is registered."""
        return device_id in self.registered_devices
    
    def _verify_sequence(self, device_id: str, sequence: int) -> bool:
        """Verify sequence number (prevent replay)."""
        if device_id not in self.device_registry:
            # First packet from this device
            self.device_registry[device_id] = sequence
            return True
        
        last_sequence = self.device_registry[device_id]
        
        # Check if sequence is ahead (normal case)
        if sequence > last_sequence:
            # Check for reasonable gap
            gap = sequence - last_sequence
            if gap <= self.max_sequence_gap:
                return True
        
        # Sequence is behind or too far ahead (possible replay or error)
        return False
    
    def _verify_signature(self, packet: Dict[str, Any]) -> bool:
        """Verify packet signature."""
        if not self.secret_key:
            return False
        
        proof = packet.get("proof", {})
        nonce = proof.get("nonce", "")
        sig = proof.get("sig", "")
        
        if not nonce or not sig:
            return False
        
        # Create expected signature
        # In production, use proper cryptographic signature verification
        device_id = packet.get("device_id", "")
        expected_sig = self._compute_signature(device_id, nonce)
        
        return hmac.compare_digest(sig, expected_sig)
    
    def _compute_signature(self, device_id: str, nonce: str) -> str:
        """Compute signature for verification."""
        if not self.secret_key:
            return ""
        
        message = f"{device_id}:{nonce}"
        return hmac.new(
            self.secret_key.encode(),
            message.encode(),
            hashlib.sha256
        ).hexdigest()
    
    def _verify_hash(self, data: Any, expected_hash: str) -> bool:
        """Verify data hash."""
        if isinstance(data, list):
            # Convert list to string for hashing
            data_str = str(data)
        else:
            data_str = str(data)
        
        computed_hash = hashlib.sha256(data_str.encode()).hexdigest()
        return hmac.compare_digest(computed_hash, expected_hash)

