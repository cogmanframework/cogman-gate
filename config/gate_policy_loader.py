"""
Gate Policy Loader (Python)

Purpose: Load and validate GATE_POLICY.yaml
"""

try:
    import yaml
except ImportError:
    yaml = None
    print("Warning: PyYAML not installed. Install with: pip install PyYAML")

from typing import Dict, Any, Optional, List
from dataclasses import dataclass, field


@dataclass
class PolicyMetadata:
    policy_name: str = "CORE-9_DECISION_GATE"
    version: str = "v1.0"
    status: str = "LOCKED"
    owner: str = "system_owner"
    decision_modes: List[str] = field(default_factory=lambda: ["ALLOW", "REVIEW", "BLOCK"])
    fail_closed: bool = True
    explainable: bool = True
    deterministic: bool = True


@dataclass
class EMuBands:
    accept_min: float = 30.0
    accept_max: float = 80.0
    caution_min: float = 15.0
    caution_max: float = 30.0
    restrict_max: float = 15.0


@dataclass
class ContextLimits:
    embedding_distance_max: float = 0.35
    entropy_max_p95: float = 0.62
    e_mu_bands: EMuBands = field(default_factory=EMuBands)
    variance_max: float = 8.0
    negative_trend_review: bool = True


@dataclass
class ContextProfile:
    name: str = ""
    description: str = ""
    limits: ContextLimits = field(default_factory=ContextLimits)


@dataclass
class GatePolicy:
    meta: PolicyMetadata = field(default_factory=PolicyMetadata)
    contexts: Dict[str, ContextProfile] = field(default_factory=dict)
    
    def get_context(self, context_name: str) -> Optional[ContextProfile]:
        """Get context profile by name."""
        return self.contexts.get(context_name)
    
    def validate(self) -> bool:
        """Validate policy structure."""
        if not self.meta.policy_name or not self.meta.version:
            return False
        
        if not self.contexts:
            return False
        
        for name, profile in self.contexts.items():
            if profile.name != name:
                return False
            
            limits = profile.limits
            if (limits.embedding_distance_max <= 0.0 or
                limits.entropy_max_p95 <= 0.0 or
                limits.variance_max <= 0.0):
                return False
            
            bands = limits.e_mu_bands
            if (bands.restrict_max >= bands.caution_min or
                bands.caution_max >= bands.accept_min or
                bands.accept_max <= bands.accept_min):
                return False
        
        return True


class GatePolicyLoader:
    """Load and validate GATE_POLICY.yaml"""
    
    @staticmethod
    def load_from_file(file_path: str) -> Optional[GatePolicy]:
        """Load policy from YAML file."""
        try:
            with open(file_path, 'r') as f:
                yaml_content = f.read()
            return GatePolicyLoader.load_from_string(yaml_content)
        except Exception as e:
            print(f"Error loading policy: {e}")
            return None
    
    @staticmethod
    def load_from_string(yaml_content: str) -> Optional[GatePolicy]:
        """Load policy from YAML string."""
        if yaml is None:
            print("Error: PyYAML not installed. Install with: pip install PyYAML")
            return None
        try:
            data = yaml.safe_load(yaml_content)
            return GatePolicyLoader._parse_yaml(data)
        except Exception as e:
            print(f"Error parsing YAML: {e}")
            return None
    
    @staticmethod
    def _parse_yaml(data: Dict[str, Any]) -> GatePolicy:
        """Parse YAML data into GatePolicy."""
        policy = GatePolicy()
        
        # Parse metadata
        if 'meta' in data:
            meta_data = data['meta']
            policy.meta = PolicyMetadata(
                policy_name=meta_data.get('policy_name', 'CORE-9_DECISION_GATE'),
                version=meta_data.get('version', 'v1.0'),
                status=meta_data.get('status', 'LOCKED'),
                owner=meta_data.get('owner', 'system_owner'),
                decision_modes=meta_data.get('decision_modes', ['ALLOW', 'REVIEW', 'BLOCK']),
                fail_closed=meta_data.get('fail_closed', True),
                explainable=meta_data.get('explainable', True),
                deterministic=meta_data.get('deterministic', True)
            )
        
        # Parse contexts
        if 'contexts' in data:
            for context_name, context_data in data['contexts'].items():
                profile = ContextProfile(name=context_name)
                
                if 'description' in context_data:
                    profile.description = context_data['description']
                
                if 'limits' in context_data:
                    limits_data = context_data['limits']
                    limits = ContextLimits()
                    
                    if 'embedding_distance' in limits_data:
                        limits.embedding_distance_max = limits_data['embedding_distance'].get('max', 0.35)
                    
                    if 'entropy' in limits_data:
                        limits.entropy_max_p95 = limits_data['entropy'].get('max_p95', 0.62)
                    
                    if 'e_mu_bands' in limits_data:
                        bands_data = limits_data['e_mu_bands']
                        bands = EMuBands()
                        
                        if 'accept' in bands_data:
                            accept_range = bands_data['accept']
                            bands.accept_min = accept_range[0]
                            bands.accept_max = accept_range[1]
                        
                        if 'caution' in bands_data:
                            caution_range = bands_data['caution']
                            bands.caution_min = caution_range[0]
                            bands.caution_max = caution_range[1]
                        
                        if 'restrict' in bands_data:
                            restrict_range = bands_data['restrict']
                            if isinstance(restrict_range, list):
                                bands.restrict_max = restrict_range[1] if len(restrict_range) > 1 else restrict_range[0]
                            else:
                                # Handle (-inf, 15) format
                                bands.restrict_max = 15.0  # Default
                        
                        limits.e_mu_bands = bands
                    
                    if 'stability' in limits_data:
                        limits.variance_max = limits_data['stability'].get('variance_max', 8.0)
                    
                    if 'trend' in limits_data:
                        limits.negative_trend_review = limits_data['trend'].get('negative_trend_review', True)
                    
                    profile.limits = limits
                
                policy.contexts[context_name] = profile
        
        return policy
    
    @staticmethod
    def validate_policy(policy: GatePolicy) -> bool:
        """Validate policy structure."""
        return policy.validate()


def create_decision_bands_from_profile(profile: ContextProfile) -> Dict[str, Any]:
    """Convert ContextProfile to decision bands dictionary."""
    limits = profile.limits
    bands = limits.e_mu_bands
    
    return {
        'context': profile.name,
        'version': '1.0',
        'D_max': limits.embedding_distance_max,
        'H_max': limits.entropy_max_p95,
        'V_max': limits.variance_max,
        'E_mu_accept_min': bands.accept_min,
        'E_mu_accept_max': bands.accept_max,
        'E_mu_caution_min': bands.caution_min,
        'E_mu_caution_max': bands.caution_max,
        'E_mu_restrict_max': bands.restrict_max,
    }


# Example usage
if __name__ == "__main__":
    policy = GatePolicyLoader.load_from_file("gate_profiles.yaml")
    
    if policy:
        print(f"Policy: {policy.meta.policy_name} v{policy.meta.version}")
        print(f"Status: {policy.meta.status}")
        print(f"\nAvailable contexts:")
        for name, profile in policy.contexts.items():
            print(f"  - {name}: {profile.description}")
            print(f"    D_max: {profile.limits.embedding_distance_max}")
            print(f"    H_max: {profile.limits.entropy_max_p95}")
            print(f"    Eμ accept: [{profile.limits.e_mu_bands.accept_min}, {profile.limits.e_mu_bands.accept_max}]")
    else:
        print("Failed to load policy")

