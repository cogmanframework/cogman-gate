"""
Kernel Bridge (ctypes)

Purpose: Bridge between Python and C++ kernel
"""

from typing import Dict, Any, Optional, List
import ctypes
import os
import sys
from pathlib import Path


class KernelBridge:
    """
    Bridge to C++ kernel.
    
    Uses ctypes to call C++ kernel functions via C ABI.
    """
    
    def __init__(self, library_path: Optional[str] = None):
        """
        Initialize kernel bridge.
        
        Args:
            library_path: Path to compiled kernel library (.so, .dylib, or .dll)
        """
        self.library = None
        if library_path:
            self.load_library(library_path)
        else:
            # Try to find library automatically
            self._auto_load_library()
    
    def _auto_load_library(self):
        """Try to find and load kernel library automatically."""
        # Common library names
        lib_names = []
        
        if sys.platform == "darwin":
            lib_names = ["libcogman_kernel.dylib", "libcogman_kernel.a"]
        elif sys.platform.startswith("linux"):
            lib_names = ["libcogman_kernel.so", "libcogman_kernel.a"]
        elif sys.platform.startswith("win"):
            lib_names = ["cogman_kernel.dll", "cogman_kernel.lib"]
        
        # Search paths
        search_paths = [
            Path(__file__).parent.parent / "kernel" / "build",
            Path(__file__).parent.parent / "kernel" / "build" / "lib",
            Path("/usr/local/lib"),
            Path("/usr/lib"),
        ]
        
        for search_path in search_paths:
            for lib_name in lib_names:
                lib_path = search_path / lib_name
                if lib_path.exists():
                    try:
                        self.load_library(str(lib_path))
                        return
                    except Exception:
                        continue
    
    def load_library(self, library_path: str):
        """
        Load kernel library.
        
        Args:
            library_path: Path to compiled kernel library
        """
        if not os.path.exists(library_path):
            raise FileNotFoundError(f"Library not found: {library_path}")
        
        try:
            self.library = ctypes.CDLL(library_path)
            self._setup_function_signatures()
        except Exception as e:
            raise RuntimeError(f"Failed to load library {library_path}: {e}")
    
    def _setup_function_signatures(self):
        """Setup ctypes function signatures for C API."""
        if not self.library:
            return
        
        # EPS8State struct
        class EPS8State(ctypes.Structure):
            _fields_ = [
                ("I", ctypes.c_double),
                ("P", ctypes.c_double),
                ("S", ctypes.c_double),
                ("H", ctypes.c_double),
                ("F", ctypes.c_double),
                ("A", ctypes.c_double),
                ("S_a", ctypes.c_double),
                ("theta", ctypes.c_double),
            ]
        
        # EnergyState struct
        class EnergyState(ctypes.Structure):
            _fields_ = [
                ("delta_E_psi", ctypes.c_double),
                ("E_reflex", ctypes.c_double),
                ("delta_E_psi_theta", ctypes.c_double),
                ("E_mind", ctypes.c_double),
                ("E_coherence", ctypes.c_double),
                ("E_neural", ctypes.c_double),
                ("E_bind", ctypes.c_double),
                ("E_mem", ctypes.c_double),
                ("verdict", ctypes.c_int),
            ]
        
        # DecisionParams struct
        class DecisionParams(ctypes.Structure):
            _fields_ = [
                ("rule_fail", ctypes.c_int),
                ("E_mu_restrict_min", ctypes.c_double),
                ("E_mu_restrict_max", ctypes.c_double),
                ("H_threshold", ctypes.c_double),
                ("D_traj_threshold", ctypes.c_double),
            ]
        
        # CoreMetrics struct
        class CoreMetrics(ctypes.Structure):
            _fields_ = [
                ("E_mu", ctypes.c_double),
                ("H", ctypes.c_double),
                ("D", ctypes.c_double),
                ("S", ctypes.c_double),
                ("T", ctypes.c_double),
                ("V", ctypes.c_double),
            ]
        
        # DecisionBands struct
        class DecisionBands(ctypes.Structure):
            _fields_ = [
                ("D_max", ctypes.c_double),
                ("H_max", ctypes.c_double),
                ("V_max", ctypes.c_double),
                ("E_mu_accept_min", ctypes.c_double),
                ("E_mu_accept_max", ctypes.c_double),
                ("E_mu_caution_min", ctypes.c_double),
                ("E_mu_caution_max", ctypes.c_double),
                ("E_mu_restrict_max", ctypes.c_double),
                ("context", ctypes.c_char * 64),
                ("version", ctypes.c_char * 16),
            ]
        
        # DecisionInput struct
        class DecisionInput(ctypes.Structure):
            _fields_ = [
                ("metrics", CoreMetrics),
                ("bands", DecisionBands),
                ("E_mu_history", ctypes.POINTER(ctypes.c_double)),
                ("E_mu_history_size", ctypes.c_int),
                ("context", ctypes.c_char * 64),
            ]
        
        # DecisionResult struct
        class DecisionResult(ctypes.Structure):
            _fields_ = [
                ("verdict", ctypes.c_int),
                ("metrics", CoreMetrics),
                ("rule_fail", ctypes.c_int),
                ("reasons", ctypes.POINTER(ctypes.c_char_p)),
                ("reasons_count", ctypes.c_int),
                ("protocol", ctypes.c_char * 32),
                ("context", ctypes.c_char * 64),
            ]
        
        # Store struct classes
        self.EPS8State = EPS8State
        self.EnergyState = EnergyState
        self.DecisionParams = DecisionParams
        self.CoreMetrics = CoreMetrics
        self.DecisionBands = DecisionBands
        self.DecisionInput = DecisionInput
        self.DecisionResult = DecisionResult
        
        # Setup cogman_energy_projection
        self.library.cogman_energy_projection.argtypes = [
            ctypes.POINTER(EPS8State),
            ctypes.POINTER(ctypes.c_double),
            ctypes.c_double,
            ctypes.c_double,
            ctypes.POINTER(DecisionParams),
            ctypes.POINTER(EnergyState),
        ]
        self.library.cogman_energy_projection.restype = ctypes.c_int
        
        # Setup cogman_decision_gate
        self.library.cogman_decision_gate.argtypes = [
            ctypes.POINTER(DecisionParams),
            ctypes.c_double,
            ctypes.c_double,
        ]
        self.library.cogman_decision_gate.restype = ctypes.c_int
        
        # Setup cogman_validate_state
        self.library.cogman_validate_state.argtypes = [
            ctypes.POINTER(EPS8State),
        ]
        self.library.cogman_validate_state.restype = ctypes.c_int
        
        # Setup cogman_core9_evaluate
        self.library.cogman_core9_evaluate.argtypes = [
            ctypes.POINTER(DecisionInput),
            ctypes.POINTER(DecisionResult),
        ]
        self.library.cogman_core9_evaluate.restype = ctypes.c_int
        
        # Setup cogman_free_decision_result
        self.library.cogman_free_decision_result.argtypes = [
            ctypes.POINTER(DecisionResult),
        ]
        self.library.cogman_free_decision_result.restype = None
    
    def energy_projection(self, eps8_state: Dict[str, float], 
                         neural_components: Dict[str, float],
                         theta_phase: float,
                         E_pred: float,
                         decision_params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Call kernel energy projection.
        
        Args:
            eps8_state: EPS-8 state dict (I, P, S, H, F, A, S_a, theta)
            neural_components: Neural components dict (dopamine, serotonin, oxytocin, adrenaline, cortisol)
            theta_phase: Theta phase value
            E_pred: Predicted energy
            decision_params: Decision parameters dict
        
        Returns:
            Energy state dictionary
        """
        if not self.library:
            raise RuntimeError("Library not loaded")
        
        # Create C structs
        c_state = self.EPS8State(
            I=eps8_state.get('I', 0.0),
            P=eps8_state.get('P', 0.0),
            S=eps8_state.get('S', 0.0),
            H=eps8_state.get('H', 0.0),
            F=eps8_state.get('F', 0.0),
            A=eps8_state.get('A', 0.0),
            S_a=eps8_state.get('S_a', 0.0),
            theta=eps8_state.get('theta', 0.0),
        )
        
        c_neural = (ctypes.c_double * 5)(
            neural_components.get('dopamine', 0.0),
            neural_components.get('serotonin', 0.0),
            neural_components.get('oxytocin', 0.0),
            neural_components.get('adrenaline', 0.0),
            neural_components.get('cortisol', 0.0),
        )
        
        c_params = self.DecisionParams(
            rule_fail=1 if decision_params.get('rule_fail', False) else 0,
            E_mu_restrict_min=decision_params.get('E_mu_restrict_min', -1e10),
            E_mu_restrict_max=decision_params.get('E_mu_restrict_max', 1e10),
            H_threshold=decision_params.get('H_threshold', 0.85),
            D_traj_threshold=decision_params.get('D_traj_threshold', 0.7),
        )
        
        c_output = self.EnergyState()
        
        # Call C function
        result = self.library.cogman_energy_projection(
            ctypes.byref(c_state),
            c_neural,
            ctypes.c_double(theta_phase),
            ctypes.c_double(E_pred),
            ctypes.byref(c_params),
            ctypes.byref(c_output),
        )
        
        if result != 0:
            raise RuntimeError(f"Energy projection failed with code {result}")
        
        # Convert verdict int to string
        verdict_map = {0: "ALLOW", 1: "REVIEW", 2: "BLOCK"}
        
        return {
            "delta_E_psi": c_output.delta_E_psi,
            "E_reflex": c_output.E_reflex,
            "delta_E_psi_theta": c_output.delta_E_psi_theta,
            "E_mind": c_output.E_mind,
            "E_coherence": c_output.E_coherence,
            "E_neural": c_output.E_neural,
            "E_bind": c_output.E_bind,
            "E_mem": c_output.E_mem,
            "verdict": verdict_map.get(c_output.verdict, "UNKNOWN"),
        }
    
    def decision_gate(self, decision_params: Dict[str, Any],
                     H_current: float,
                     D_traj_current: float = 0.0) -> str:
        """
        Call decision gate.
        
        Args:
            decision_params: Decision parameters dict
            H_current: Current entropy value
            D_traj_current: Current trajectory distance
        
        Returns:
            Verdict string ("ALLOW", "REVIEW", or "BLOCK")
        """
        if not self.library:
            raise RuntimeError("Library not loaded")
        
        c_params = self.DecisionParams(
            rule_fail=1 if decision_params.get('rule_fail', False) else 0,
            E_mu_restrict_min=decision_params.get('E_mu_restrict_min', -1e10),
            E_mu_restrict_max=decision_params.get('E_mu_restrict_max', 1e10),
            H_threshold=decision_params.get('H_threshold', 0.85),
            D_traj_threshold=decision_params.get('D_traj_threshold', 0.7),
        )
        
        verdict = self.library.cogman_decision_gate(
            ctypes.byref(c_params),
            ctypes.c_double(H_current),
            ctypes.c_double(D_traj_current),
        )
        
        verdict_map = {0: "ALLOW", 1: "REVIEW", 2: "BLOCK"}
        return verdict_map.get(verdict, "UNKNOWN")
    
    def validate_state(self, eps8_state: Dict[str, float]) -> bool:
        """
        Validate EPS-8 state.
        
        Args:
            eps8_state: EPS-8 state dict
        
        Returns:
            True if valid, False otherwise
        """
        if not self.library:
            raise RuntimeError("Library not loaded")
        
        c_state = self.EPS8State(
            I=eps8_state.get('I', 0.0),
            P=eps8_state.get('P', 0.0),
            S=eps8_state.get('S', 0.0),
            H=eps8_state.get('H', 0.0),
            F=eps8_state.get('F', 0.0),
            A=eps8_state.get('A', 0.0),
            S_a=eps8_state.get('S_a', 0.0),
            theta=eps8_state.get('theta', 0.0),
        )
        
        result = self.library.cogman_validate_state(ctypes.byref(c_state))
        return result == 1
    
    def core9_evaluate(self, metrics: Dict[str, float],
                      bands: Dict[str, Any],
                      context: str = "default",
                      E_mu_history: Optional[List[float]] = None) -> Dict[str, Any]:
        """
        Call CORE-9 decision gate (production spec).
        
        Args:
            metrics: Core metrics dict (E_mu, H, D, S, T, V)
            bands: Decision bands dict
            context: Context name
            E_mu_history: Optional Eμ history for trend/variance calculation
        
        Returns:
            Decision result dictionary
        """
        if not self.library:
            raise RuntimeError("Library not loaded")
        
        # Create CoreMetrics
        c_metrics = self.CoreMetrics(
            E_mu=metrics.get('E_mu', 0.0),
            H=metrics.get('H', 0.0),
            D=metrics.get('D', 0.0),
            S=metrics.get('S', 1.0),
            T=metrics.get('T', 0.0),
            V=metrics.get('V', 0.0),
        )
        
        # Create DecisionBands
        c_bands = self.DecisionBands(
            D_max=bands.get('D_max', 0.35),
            H_max=bands.get('H_max', 0.62),
            V_max=bands.get('V_max', 8.0),
            E_mu_accept_min=bands.get('E_mu_accept_min', 30.0),
            E_mu_accept_max=bands.get('E_mu_accept_max', 80.0),
            E_mu_caution_min=bands.get('E_mu_caution_min', 15.0),
            E_mu_caution_max=bands.get('E_mu_caution_max', 30.0),
            E_mu_restrict_max=bands.get('E_mu_restrict_max', 15.0),
            context=context.encode('utf-8')[:63],
            version=b"1.0",
        )
        
        # Create Eμ history array
        c_history_ptr = None
        c_history_size = 0
        if E_mu_history:
            c_history_size = len(E_mu_history)
            c_history_array = (ctypes.c_double * c_history_size)(*E_mu_history)
            c_history_ptr = ctypes.cast(c_history_array, ctypes.POINTER(ctypes.c_double))
        
        # Create DecisionInput
        c_input = self.DecisionInput(
            metrics=c_metrics,
            bands=c_bands,
            E_mu_history=c_history_ptr,
            E_mu_history_size=c_history_size,
            context=context.encode('utf-8')[:63],
        )
        
        # Create DecisionResult
        c_output = self.DecisionResult()
        
        # Call C function
        result = self.library.cogman_core9_evaluate(
            ctypes.byref(c_input),
            ctypes.byref(c_output),
        )
        
        if result != 0:
            raise RuntimeError(f"CORE-9 evaluation failed with code {result}")
        
        # Convert reasons array to Python list
        reasons = []
        if c_output.reasons and c_output.reasons_count > 0:
            for i in range(c_output.reasons_count):
                if c_output.reasons[i]:
                    reasons.append(c_output.reasons[i].decode('utf-8'))
        
        # Build result dict
        verdict_map = {0: "ALLOW", 1: "REVIEW", 2: "BLOCK"}
        decision_result = {
            "verdict": verdict_map.get(c_output.verdict, "UNKNOWN"),
            "metrics": {
                "E_mu": c_output.metrics.E_mu,
                "H": c_output.metrics.H,
                "D": c_output.metrics.D,
                "S": c_output.metrics.S,
                "T": c_output.metrics.T,
                "V": c_output.metrics.V,
            },
            "rule_fail": c_output.rule_fail != 0,
            "reasons": reasons,
            "protocol": c_output.protocol.decode('utf-8'),
            "context": c_output.context.decode('utf-8'),
        }
        
        # Free C memory
        self.library.cogman_free_decision_result(ctypes.byref(c_output))
        
        return decision_result
