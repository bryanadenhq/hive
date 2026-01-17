"""
Type definitions for Aden Tools.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional, Union


# Type aliases
ToolResult = Union[str, Dict[str, Any]]


@dataclass
class EnvVar:
    """Environment variable specification for a tool."""

    name: str
    description: str
    required: bool = True
    default: Optional[str] = None


@dataclass
class ToolOutput:
    """Standardized tool output wrapper."""

    success: bool
    data: Any = None
    error: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert output to dictionary format."""
        result: Dict[str, Any] = {"success": self.success}
        if self.data is not None:
            result["data"] = self.data
        if self.error is not None:
            result["error"] = self.error
        return result
