"""
Annotation

Purpose: Annotate with LLM
"""

from typing import Dict, Any


class Annotation:
    """
    LLM annotation interface.
    """
    
    def annotate(self, content: str, context: Dict[str, Any] = None) -> str:
        """
        Annotate content with LLM.
        
        Returns:
            Annotated content
        """
        # Placeholder: Return as-is
        return content

