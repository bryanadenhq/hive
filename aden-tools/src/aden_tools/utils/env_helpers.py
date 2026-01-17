"""
Environment variable helpers for Aden Tools.
"""
from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from ..tool_types import EnvVar


def get_env_var(
    name: str,
    default: Optional[str] = None,
    required: bool = False,
) -> Optional[str]:
    """
    Get an environment variable with optional default and required validation.

    Args:
        name: Name of the environment variable
        default: Default value if not set
        required: If True, raises ValueError when not set and no default

    Returns:
        The environment variable value or default

    Raises:
        ValueError: If required=True and variable is not set with no default
    """
    value = os.environ.get(name, default)
    if required and value is None:
        raise ValueError(
            f"Required environment variable '{name}' is not set. "
            f"Please set it before using this tool."
        )
    return value


def validate_env_vars(env_vars: List[EnvVar]) -> Dict[str, Any]:
    """
    Validate and retrieve all environment variables for a tool.

    Args:
        env_vars: List of EnvVar specifications

    Returns:
        Dictionary mapping variable names to their values

    Raises:
        ValueError: If any required variable is missing
    """
    missing: List[str] = []
    values: Dict[str, Any] = {}

    for env_var in env_vars:
        value = os.environ.get(env_var.name, env_var.default)

        if value is None and env_var.required:
            missing.append(env_var.name)
        else:
            values[env_var.name] = value

    if missing:
        missing_str = ", ".join(missing)
        raise ValueError(
            f"Missing required environment variables: {missing_str}. "
            "Please set these variables before using this tool."
        )

    return values
