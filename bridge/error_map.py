"""
Error Mapping

Purpose: Map C++ kernel errors to Python exceptions
"""


class KernelError(Exception):
    """Base exception for kernel errors."""
    pass


class InvalidStateError(KernelError):
    """Invalid state error."""
    pass


class ComputationError(KernelError):
    """Computation error."""
    pass


def map_kernel_error(error_code: int, message: str = "") -> Exception:
    """
    Map C++ kernel error code to Python exception.
    
    Args:
        error_code: C++ error code
        message: Error message
    
    Returns:
        Python exception
    """
    if error_code == -1:
        return InvalidStateError(f"Invalid state: {message}")
    elif error_code < 0:
        return ComputationError(f"Computation error (code {error_code}): {message}")
    else:
        return KernelError(f"Unknown error (code {error_code}): {message}")

