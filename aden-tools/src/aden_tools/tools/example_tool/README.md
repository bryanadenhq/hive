# Example Tool

A template tool demonstrating the Aden tools pattern.

## Description

This tool processes text messages with optional transformations. It serves as a reference implementation for creating new tools.

## Usage

```python
from aden_tools import ExampleTool

tool = ExampleTool()

# Basic usage
result = tool.run(message="Hello World")
# Returns: "Hello World"

# With uppercase
result = tool.run(message="Hello World", uppercase=True)
# Returns: "HELLO WORLD"

# With repetition
result = tool.run(message="Hi", repeat=3)
# Returns: "Hi Hi Hi"

# Combined
result = tool.run(message="Hello", uppercase=True, repeat=2)
# Returns: "HELLO HELLO"
```

## Arguments

| Argument | Type | Required | Default | Description |
|----------|------|----------|---------|-------------|
| `message` | str | Yes | - | The message to process (1-1000 chars) |
| `uppercase` | bool | No | False | Convert message to uppercase |
| `repeat` | int | No | 1 | Number of times to repeat (1-10) |

## Environment Variables

This tool does not require any environment variables.

## Error Handling

The tool returns error messages as strings rather than raising exceptions, making it safe for agent use.
