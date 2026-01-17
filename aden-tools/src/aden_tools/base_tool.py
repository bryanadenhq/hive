"""
Base Tool class for the Aden agent framework.

All tools should inherit from BaseTool and implement the _run method.
"""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Type

from pydantic import BaseModel, Field

from .tool_types import EnvVar, ToolResult


class BaseTool(BaseModel, ABC):
    """
    Abstract base class for all Aden tools.

    Subclasses must:
    - Set `name` and `description` attributes
    - Define `args_schema` as a Pydantic model for input validation
    - Implement the `_run()` method

    Example:
        class MyToolSchema(BaseModel):
            query: str = Field(..., description="The search query")

        class MyTool(BaseTool):
            name: str = "my_tool"
            description: str = "Performs a search operation"
            args_schema: Type[BaseModel] = MyToolSchema

            def _run(self, query: str) -> str:
                return f"Results for: {query}"
    """

    model_config = {"arbitrary_types_allowed": True}

    name: str = Field(..., description="Unique identifier for the tool")
    description: str = Field(
        ..., description="Description of what the tool does and when to use it"
    )
    args_schema: Optional[Type[BaseModel]] = Field(
        default=None, description="Pydantic model defining the tool's input schema"
    )
    env_vars: List[EnvVar] = Field(
        default_factory=list,
        description="Environment variables required by this tool",
    )
    cache_function: Optional[Callable[[Any], bool]] = Field(
        default=None, description="Function to determine if result should be cached"
    )
    result_as_answer: bool = Field(
        default=False,
        description="If True, the tool output becomes the final agent response",
    )
    max_usage_count: Optional[int] = Field(
        default=None, description="Maximum number of times this tool can be used"
    )
    _current_usage_count: int = 0

    @abstractmethod
    def _run(self, **kwargs: Any) -> ToolResult:
        """
        Execute the tool's main logic.

        Subclasses must implement this method.

        Args:
            **kwargs: Arguments matching the args_schema

        Returns:
            Tool result as string or dict
        """
        pass

    async def _arun(self, **kwargs: Any) -> ToolResult:
        """
        Async version of _run.

        Override this method to provide async support.
        Default implementation raises NotImplementedError.

        Args:
            **kwargs: Arguments matching the args_schema

        Returns:
            Tool result as string or dict
        """
        raise NotImplementedError(
            f"Async execution not implemented for {self.name}. "
            "Override _arun() to add async support."
        )

    def run(self, **kwargs: Any) -> ToolResult:
        """
        Execute the tool with usage tracking and validation.

        Args:
            **kwargs: Arguments to pass to _run

        Returns:
            Tool result

        Raises:
            RuntimeError: If max usage count exceeded
            ValidationError: If arguments don't match schema
        """
        # Check usage limit
        if self.max_usage_count is not None:
            if self._current_usage_count >= self.max_usage_count:
                raise RuntimeError(
                    f"Tool '{self.name}' has reached its maximum usage count "
                    f"of {self.max_usage_count}"
                )

        # Validate arguments if schema is defined
        if self.args_schema is not None:
            self.args_schema(**kwargs)

        # Execute and track usage
        self._current_usage_count += 1
        return self._run(**kwargs)

    async def arun(self, **kwargs: Any) -> ToolResult:
        """
        Execute the tool asynchronously with usage tracking.

        Args:
            **kwargs: Arguments to pass to _arun

        Returns:
            Tool result
        """
        # Check usage limit
        if self.max_usage_count is not None:
            if self._current_usage_count >= self.max_usage_count:
                raise RuntimeError(
                    f"Tool '{self.name}' has reached its maximum usage count "
                    f"of {self.max_usage_count}"
                )

        # Validate arguments if schema is defined
        if self.args_schema is not None:
            self.args_schema(**kwargs)

        # Execute and track usage
        self._current_usage_count += 1
        return await self._arun(**kwargs)

    def reset_usage_count(self) -> None:
        """Reset the usage counter to zero."""
        self._current_usage_count = 0

    @property
    def current_usage_count(self) -> int:
        """Get the current usage count."""
        return self._current_usage_count

    def get_schema_dict(self) -> Dict[str, Any]:
        """
        Get the tool's input schema as a dictionary.

        Returns:
            JSON schema dict or empty dict if no schema defined
        """
        if self.args_schema is None:
            return {}
        return self.args_schema.model_json_schema()

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(name={self.name!r})>"
