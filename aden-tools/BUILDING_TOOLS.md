# Building Tools for Aden

This guide explains how to create new tools for the Aden agent framework.

## Quick Start Checklist

1. Create folder under `src/aden_tools/tools/<tool_name>/`
2. Implement class extending `BaseTool` with `args_schema`
3. Declare `env_vars` if your tool needs environment variables
4. Implement `_run()` and optionally `_arun()` for async
5. Add a `README.md` documenting your tool
6. Export from `src/aden_tools/tools/__init__.py`
7. Add tests in `tests/tools/`

## Tool Structure

Each tool lives in its own folder:

```
src/aden_tools/tools/my_tool/
├── __init__.py           # Export the tool class
├── my_tool.py            # Tool implementation
└── README.md             # Documentation
```

## Implementation Pattern

### 1. Define Input Schema

Use Pydantic to define your tool's input parameters:

```python
from pydantic import BaseModel, Field

class MyToolSchema(BaseModel):
    """Input schema for MyTool."""

    query: str = Field(
        ...,  # Required
        description="The search query",
        min_length=1,
        max_length=500,
    )
    limit: int = Field(
        default=10,
        description="Maximum number of results",
        ge=1,
        le=100,
    )
```

### 2. Implement the Tool Class

```python
from aden_tools import BaseTool, EnvVar

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = (
        "Searches for items matching a query. "
        "Use this when you need to find specific information."
    )
    args_schema: type[BaseModel] = MyToolSchema

    # Optional: declare required environment variables
    env_vars: list[EnvVar] = [
        EnvVar(
            name="MY_API_KEY",
            description="API key for the service",
            required=True,
        ),
    ]

    def _run(self, query: str, limit: int = 10, **kwargs) -> str:
        """Execute the tool."""
        try:
            # Your implementation here
            results = self._search(query, limit)
            return f"Found {len(results)} results"
        except Exception as e:
            return f"Error: {str(e)}"

    async def _arun(self, query: str, limit: int = 10, **kwargs) -> str:
        """Async version (optional)."""
        # Async implementation
        pass
```

### 3. Export the Tool

In `src/aden_tools/tools/my_tool/__init__.py`:
```python
from .my_tool import MyTool, MyToolSchema

__all__ = ["MyTool", "MyToolSchema"]
```

In `src/aden_tools/tools/__init__.py`:
```python
from .my_tool import MyTool, MyToolSchema

__all__ = [
    # ... existing tools
    "MyTool",
    "MyToolSchema",
]
```

## Required Attributes

| Attribute | Type | Description |
|-----------|------|-------------|
| `name` | str | Unique identifier (snake_case) |
| `description` | str | What the tool does and when to use it |
| `args_schema` | type[BaseModel] | Pydantic model for input validation |

## Optional Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `env_vars` | list[EnvVar] | [] | Required environment variables |
| `max_usage_count` | int \| None | None | Limit tool usage |
| `result_as_answer` | bool | False | Use result as final answer |
| `cache_function` | Callable | None | Caching logic |

## Best Practices

### Error Handling

Return helpful error messages instead of raising exceptions:

```python
def _run(self, **kwargs) -> str:
    try:
        result = self._do_work()
        return result
    except SpecificError as e:
        return f"Failed to process: {str(e)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
```

### Environment Variables

Validate credentials early in `__init__` if needed:

```python
def __init__(self, **kwargs):
    super().__init__(**kwargs)
    from aden_tools import validate_env_vars
    self._env = validate_env_vars(self.env_vars)
```

### Return Values

- Return strings for simple results
- Return dicts for structured data (will be JSON-serialized)
- Keep output concise and deterministic

### Documentation

Every tool needs a `README.md` with:
- Description and use cases
- Usage examples
- Argument table
- Environment variables (if any)
- Error handling notes

## Testing

Place tests in `tests/tools/test_my_tool.py`:

```python
import pytest
from aden_tools.tools import MyTool

def test_my_tool_basic():
    tool = MyTool()
    result = tool.run(query="test")
    assert "results" in result

def test_my_tool_validation():
    tool = MyTool()
    with pytest.raises(ValueError):
        tool.run(query="")  # Empty query should fail
```

Mock external APIs to keep tests fast and deterministic.

## Naming Conventions

- **Folder name**: `snake_case` (e.g., `file_read_tool`)
- **Class name**: `PascalCase` ending in `Tool` (e.g., `FileReadTool`)
- **Tool name attribute**: `snake_case` (e.g., `file_read`)
