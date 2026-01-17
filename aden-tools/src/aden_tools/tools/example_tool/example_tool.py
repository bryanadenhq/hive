"""
Example Tool - A template demonstrating the Aden tool pattern.

This tool serves as a reference implementation showing:
- How to define input schemas with Pydantic
- How to implement the _run method
- How to handle errors properly
- How to document your tool
"""
from __future__ import annotations

from typing import Any, Type

from pydantic import BaseModel, Field

from ...base_tool import BaseTool
from ...tool_types import ToolResult


class ExampleToolSchema(BaseModel):
    """Input schema for ExampleTool."""

    message: str = Field(
        ...,
        description="The message to process",
        min_length=1,
        max_length=1000,
    )
    uppercase: bool = Field(
        default=False,
        description="If True, convert the message to uppercase",
    )
    repeat: int = Field(
        default=1,
        description="Number of times to repeat the message",
        ge=1,
        le=10,
    )


class ExampleTool(BaseTool):
    """
    Example tool that processes a message.

    This is a template tool demonstrating the correct pattern for
    creating tools in the Aden framework. Use this as a starting
    point for your own tools.

    Example usage:
        tool = ExampleTool()
        result = tool.run(message="Hello", uppercase=True, repeat=2)
        # Returns: "HELLO HELLO"
    """

    name: str = "example_tool"
    description: str = (
        "A simple example tool that processes text messages. "
        "Use this tool when you need to transform or repeat text."
    )
    args_schema: Type[BaseModel] = ExampleToolSchema

    def _run(
        self,
        message: str,
        uppercase: bool = False,
        repeat: int = 1,
        **kwargs: Any,
    ) -> ToolResult:
        """
        Process the message according to the specified options.

        Args:
            message: The text message to process
            uppercase: Whether to convert to uppercase
            repeat: Number of times to repeat

        Returns:
            The processed message string
        """
        try:
            # Process the message
            result = message
            if uppercase:
                result = result.upper()

            # Repeat if requested
            if repeat > 1:
                result = " ".join([result] * repeat)

            return result

        except Exception as e:
            # Return helpful error message instead of raising
            return f"Error processing message: {str(e)}"
