"""
Interface Only

Purpose: LLM interface (annotation, prompts, formatting)
"""

from .annotation import Annotation
from .prompt_templates import PromptTemplates
from .response_formatter import ResponseFormatter

__all__ = [
    'Annotation',
    'PromptTemplates',
    'ResponseFormatter',
]

