"""
Example: Post-Processor Integration

Purpose: Demonstrate Post-Processor integration with Runtime Loop PHASE 9
"""

import logging
import time
from runtime import PostProcessor, PostProcessInput
from action import ActionOutput

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def example_post_processing():
    """Example: Post-processing operations."""
    logger.info("=== Example: Post-Processor Operations ===")
    
    # Create post-processor
    post_processor = PostProcessor(
        audit_storage_path="storage/audit",
        metrics_storage_path="storage/runtime",
        enable_async=True
    )
    
    # Create test trajectory
    trajectory = {
        "trace_id": "test_trace_001",
        "states": [
            {"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3, "A": 0.5, "S_a": 0.4, "theta": 1.2},
            {"I": 0.8, "P": 0.7, "S": 0.9, "H": 0.2, "A": 0.6, "S_a": 0.5, "theta": 1.3}
        ],
        "origin": {
            "source_id": "test_source",
            "modality": "text",
            "adapter": "test_adapter"
        },
        "verdict": "ALLOW"
    }
    
    # Create test action output
    action_output = ActionOutput(
        action_type="text",
        output_data="Test output",
        trace_id="test_trace_001",
        timestamp=time.time(),
        success=True
    )
    
    # Create phase results
    phase_results = {
        "phase_times": {
            "perception": 0.01,
            "gate": 0.02,
            "wm_controller": 0.03,
            "reasoning": 0.02,
            "decision": 0.01,
            "action": 0.01
        },
        "gate_verdict": "ALLOW",
        "transformations": [
            {"module": "perception", "timestamp": time.time()},
            {"module": "wm_controller", "timestamp": time.time()},
            {"module": "reasoning", "timestamp": time.time()},
            {"module": "action", "timestamp": time.time()}
        ]
    }
    
    # Process post-processing
    post_processor.process(
        trajectory=trajectory,
        action_output=action_output,
        phase_results=phase_results
    )
    
    logger.info("Post-processing queued (async)")
    
    # Wait a bit for async processing
    time.sleep(0.1)
    
    # Shutdown (wait for async operations)
    post_processor.shutdown()
    logger.info("Post-processing completed")


def example_metrics_collection():
    """Example: Metrics collection."""
    logger.info("\n=== Example: Metrics Collection ===")
    
    # Create post-processor
    post_processor = PostProcessor(enable_async=False)  # Synchronous for testing
    
    # Create test data
    trajectory = {
        "trace_id": "test_trace_002",
        "states": [{"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3}],
        "verdict": "ALLOW"
    }
    
    action_output = ActionOutput(
        action_type="text",
        output_data="Test",
        trace_id="test_trace_002",
        timestamp=time.time(),
        success=True
    )
    
    phase_results = {
        "phase_times": {
            "perception": 0.01,
            "gate": 0.02,
            "wm_controller": 0.03,
            "reasoning": 0.02,
            "decision": 0.01,
            "action": 0.01
        },
        "gate_verdict": "ALLOW"
    }
    
    # Process
    post_processor.process(trajectory, action_output, phase_results)
    
    logger.info("Metrics collected and stored")


def example_audit_trail():
    """Example: Audit trail storage."""
    logger.info("\n=== Example: Audit Trail Storage ===")
    
    # Create post-processor
    post_processor = PostProcessor(enable_async=False)
    
    # Create test data with complete lineage
    trajectory = {
        "trace_id": "test_trace_003",
        "states": [
            {"I": 0.7, "P": 0.6, "S": 0.8, "H": 0.3, "A": 0.5, "S_a": 0.4, "theta": 1.2}
        ],
        "origin": {
            "source_id": "sensory",
            "modality": "text",
            "adapter": "text_adapter"
        },
        "verdict": "ALLOW"
    }
    
    action_output = ActionOutput(
        action_type="text",
        output_data="Audit test output",
        trace_id="test_trace_003",
        timestamp=time.time(),
        success=True
    )
    
    phase_results = {
        "transformations": [
            {"module": "perception", "operation": "energy_projection", "timestamp": time.time()},
            {"module": "gate", "operation": "admission", "timestamp": time.time()},
            {"module": "wm_controller", "operation": "routing", "timestamp": time.time()},
            {"module": "reasoning", "operation": "structure_creation", "timestamp": time.time()},
            {"module": "action", "operation": "execution", "timestamp": time.time()}
        ]
    }
    
    # Process
    post_processor.process(trajectory, action_output, phase_results)
    
    logger.info("Audit trail stored")


if __name__ == "__main__":
    example_post_processing()
    example_metrics_collection()
    example_audit_trail()

