"""
Helper functions in use for validating data entries
"""

from collections.abc import Callable
from typing import Any

from pydantic import model_validator


def validate_pair_rule(
    field1: str, field2: str, predicate: Callable[[Any, Any], bool], error_msg: str
):
    """
    Generic model validator decorator using Python match/case to safely extract
    and narrow two optional fields before evaluating a rule predicate.
    """

    def decorator(cls):
        def validator(self):
            val1 = getattr(self, field1, None)
            val2 = getattr(self, field2, None)

            match (val1, val2):
                case (v1, v2) if v1 is not None and v2 is not None:
                    if not predicate(v1, v2):
                        raise ValueError(error_msg)
                case _:
                    pass
            return self

        return model_validator(mode="after")(validator)

    return decorator


def sanitize_empty_string(val: Any) -> Any | None:
    """Helper for cleaning up empty or whitespace-only strings."""
    match val:
        case str() if not val.strip():
            return None
        case _:
            return val
