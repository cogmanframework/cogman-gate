"""
Energy Estimator Module

Purpose: Estimate IPSH state from feature vectors
"""

from typing import Optional, Dict, Any
from dataclasses import dataclass
import numpy as np
import math


@dataclass
class IPSHState:
    """IPSH State (Intensity, Polarity, Stability, Entropy)"""
    I: float  # Intensity [0, 1]
    P: float  # Polarity [0, 1]
    S: float  # Stability [0, 1]
    H: float  # Entropy [0, 1]
    dE: float  # Decision Energy


class EnergyEstimator:
    """
    Energy estimator for feature vectors.
    
    Computes IPSH state from feature vectors.
    """
    
    def __init__(self,
                 mu_I: float = 0.5,
                 sigma_I: float = 0.3,
                 lambda_stability: float = 1.0):
        """
        Initialize energy estimator.
        
        Args:
            mu_I: Mean intensity for normalization
            sigma_I: Standard deviation for intensity normalization
            lambda_stability: Stability decay parameter
        """
        self.mu_I = mu_I
        self.sigma_I = sigma_I
        self.lambda_stability = lambda_stability
    
    def estimate(self, 
                 phi_t: np.ndarray,
                 phi_prev: Optional[np.ndarray] = None) -> IPSHState:
        """
        Estimate IPSH state from feature vector.
        
        Args:
            phi_t: Current feature vector (d-dimensional)
            phi_prev: Previous feature vector (optional)
        
        Returns:
            IPSHState with computed parameters
        """
        # Convert to numpy array if needed
        if not isinstance(phi_t, np.ndarray):
            phi_t = np.array(phi_t, dtype=np.float64)
        
        if phi_prev is not None and not isinstance(phi_prev, np.ndarray):
            phi_prev = np.array(phi_prev, dtype=np.float64)
        
        # 1. Calculate Intensity
        I_t = self._calculate_intensity(phi_t)
        
        # 2. Calculate Polarity
        P_t = self._calculate_polarity(phi_t, phi_prev)
        
        # 3. Calculate Stability
        S_t = self._calculate_stability(phi_t, phi_prev)
        
        # 4. Calculate Entropy
        H_t = self._calculate_entropy(phi_t)
        
        # 5. Calculate Decision Energy
        dE = I_t * P_t * S_t * (1.0 - H_t)
        
        return IPSHState(
            I=I_t,
            P=P_t,
            S=S_t,
            H=H_t,
            dE=dE
        )
    
    def _calculate_intensity(self, phi_t: np.ndarray) -> float:
        """
        Calculate Intensity: I_t = clip((||φ_t|| - μ_I) / σ_I)
        """
        # Compute L2 norm
        norm = np.linalg.norm(phi_t)
        
        # Normalize
        I = (norm - self.mu_I) / self.sigma_I
        
        # Clip to [0, 1]
        I = max(0.0, min(1.0, I))
        
        return float(I)
    
    def _calculate_polarity(self, 
                           phi_t: np.ndarray,
                           phi_prev: Optional[np.ndarray]) -> float:
        """
        Calculate Polarity: P_t = tanh(mean(Δφ_t)) normalized to [0, 1]
        """
        if phi_prev is None:
            # No previous vector, use zeros
            delta_phi = phi_t
        else:
            # Ensure same dimension
            if phi_t.shape != phi_prev.shape:
                # Use zeros if dimensions don't match
                delta_phi = phi_t
            else:
                delta_phi = phi_t - phi_prev
        
        # Compute mean of delta
        mean_delta = np.mean(delta_phi)
        
        # Apply tanh
        P = np.tanh(mean_delta)
        
        # Normalize to [0, 1]
        P = (P + 1.0) / 2.0
        
        return float(P)
    
    def _calculate_stability(self,
                            phi_t: np.ndarray,
                            phi_prev: Optional[np.ndarray]) -> float:
        """
        Calculate Stability: S_t = exp(-λ × Var(Δφ_t))
        """
        if phi_prev is None:
            # No previous vector, assume stable
            return 1.0
        
        # Ensure same dimension
        if phi_t.shape != phi_prev.shape:
            return 0.5  # Default stability if dimensions don't match
        
        # Compute delta
        delta_phi = phi_t - phi_prev
        
        # Compute variance
        variance = np.var(delta_phi)
        
        # Compute stability
        S = math.exp(-self.lambda_stability * variance)
        
        # Ensure in [0, 1]
        S = max(0.0, min(1.0, S))
        
        return float(S)
    
    def _calculate_entropy(self, phi_t: np.ndarray) -> float:
        """
        Calculate Entropy: H_t = -Σ p_i log(p_i) normalized to [0, 1]
        """
        d = len(phi_t)
        if d == 0:
            return 0.0
        
        # Compute absolute values
        abs_phi = np.abs(phi_t)
        
        # Compute sum
        sum_abs = np.sum(abs_phi)
        
        if sum_abs == 0.0:
            # All zeros, entropy is maximum
            return 1.0
        
        # Compute probabilities
        p = abs_phi / sum_abs
        
        # Compute entropy: H = -Σ p_i log(p_i)
        # Avoid log(0) by using small epsilon
        epsilon = 1e-10
        H = -np.sum(p * np.log(p + epsilon))
        
        # Normalize to [0, 1] by dividing by log(d)
        H_normalized = H / math.log(d) if d > 1 else 0.0
        
        # Ensure in [0, 1]
        H_normalized = max(0.0, min(1.0, H_normalized))
        
        return float(H_normalized)

