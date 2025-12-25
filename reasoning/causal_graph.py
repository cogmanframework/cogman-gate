"""
Causal Graph

Purpose: Build causal graph structure
"""

from typing import Dict, Any, List


class CausalGraph:
    """
    Causal graph builder.
    
    Builds causal structure (NO FORMULA).
    """
    
    def __init__(self):
        """Initialize causal graph."""
        self.nodes: List[Dict[str, Any]] = []
        self.edges: List[Dict[str, Any]] = []
    
    def add_node(self, node: Dict[str, Any]):
        """Add node to graph."""
        self.nodes.append(node)
    
    def add_edge(self, source: str, target: str, relation: str):
        """Add edge to graph."""
        self.edges.append({
            "source": source,
            "target": target,
            "relation": relation,
        })
    
    def build(self) -> Dict[str, Any]:
        """Build causal graph."""
        return {
            "nodes": self.nodes,
            "edges": self.edges,
        }

