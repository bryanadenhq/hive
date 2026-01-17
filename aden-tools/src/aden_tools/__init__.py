"""
Aden Tools - Tool library for the Aden agent framework.

Tools provide capabilities that AI agents can use to interact with
external systems, process data, and perform actions.

Basic usage:
    from aden_tools import BaseTool, ExampleTool

    # Use a built-in tool
    tool = ExampleTool()
    result = tool.run(message="Hello")

    # Create a custom tool
    class MyTool(BaseTool):
        name = "my_tool"
        description = "Does something useful"

        def _run(self, **kwargs):
            return "result"
"""

__version__ = "0.1.0"

# Core classes
from .base_tool import BaseTool
from .tool_types import EnvVar, ToolOutput, ToolResult

# Utilities
from .utils import get_env_var, validate_env_vars

# Tools
from .tools import ExampleTool, ExampleToolSchema

__all__ = [
    # Version
    "__version__",
    # Core
    "BaseTool",
    "EnvVar",
    "ToolOutput",
    "ToolResult",
    # Utilities
    "get_env_var",
    "validate_env_vars",
    # Tools
    "ExampleTool",
    "ExampleToolSchema",
]
