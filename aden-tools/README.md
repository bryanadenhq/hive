# Aden Tools

Tool library for the Aden agent framework. Provides a collection of tools that AI agents can use to interact with external systems, process data, and perform actions.

## Installation

```bash
pip install -e aden-tools
```

For development:
```bash
pip install -e "aden-tools[dev]"
```

## Quick Start

```python
from aden_tools import ExampleTool

# Create and use a tool
tool = ExampleTool()
result = tool.run(message="Hello World", uppercase=True)
print(result)  # "HELLO WORLD"
```

## Creating Custom Tools

```python
from pydantic import BaseModel, Field
from aden_tools import BaseTool

class MyToolSchema(BaseModel):
    """Input schema for MyTool."""
    query: str = Field(..., description="The search query")
    limit: int = Field(default=10, description="Max results")

class MyTool(BaseTool):
    name: str = "my_tool"
    description: str = "Searches for items matching the query"
    args_schema: type[BaseModel] = MyToolSchema

    def _run(self, query: str, limit: int = 10, **kwargs) -> str:
        # Your tool logic here
        return f"Found {limit} results for: {query}"
```

## Available Tools

| Tool | Description |
|------|-------------|
| `ExampleTool` | Template tool demonstrating the pattern |

## Project Structure

```
aden-tools/
├── src/aden_tools/
│   ├── __init__.py          # Main exports
│   ├── base_tool.py         # BaseTool class
│   ├── tool_types.py        # Type definitions
│   ├── adapters/            # Framework adapters
│   ├── utils/               # Utility functions
│   └── tools/               # Tool implementations
│       └── example_tool/    # Example tool
├── tests/                   # Test suite
├── README.md
├── BUILDING_TOOLS.md        # Tool development guide
└── pyproject.toml
```

## Documentation

- [Building Tools Guide](BUILDING_TOOLS.md) - How to create new tools
- Individual tool READMEs in `src/aden_tools/tools/*/README.md`

## License

MIT
