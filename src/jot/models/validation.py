"""
Helper functions in use for validating data entries
"""

import contextlib
import json
from collections.abc import Mapping
from enum import Enum
from typing import Any, Self, TypeVar

from pydantic import BaseModel, ConfigDict, HttpUrl, TypeAdapter, model_validator

T = TypeVar("T", bound=type[BaseModel])


class FormModel(BaseModel):
    """
    Normalize form inputs for validating PUT/POST requests by converting
    empty strings or whitespace-only strings to None before field parsing

    Attributes:
            model_config: Strips leading/trailing whitespace from strings
    """

    model_config = ConfigDict(str_strip_whitespace=True)

    @model_validator(mode="before")
    @classmethod
    def blank_to_none(cls, data: Any) -> Any:
        """Flattens empty strings in form responses (e.g., request.form) to None"""
        if isinstance(data, Mapping):
            return {
                k: None if isinstance(v, str) and not v.strip() else v
                for k, v in data.items()
            }
        return data

    def to_params(self, *, exclude_none: bool = False) -> dict[str, Any]:
        """Serialize model fields into a MySQL-compatible parameter dictionary"""
        raw = self.model_dump(exclude_none=exclude_none)
        params: dict[str, Any] = {}

        for key, val in raw.items():
            match val:
                case Enum():
                    params[key] = val.value
                case dict() | list():
                    params[key] = json.dumps(val)
                case _:
                    params[key] = val

        return params


class RowModel(BaseModel):
    """
    Immutable model for read/query projections from the database, ignoring extra query columns (like metadata)

    Attributes:
        model_config:
            - Makes row instances immutable (frozen=True)
            - Drops unmapped columns from SELECT queries (extra="ignore")
            - Allows instantiation from row attributes
    """

    model_config = ConfigDict(frozen=True, extra="ignore", from_attributes=True)

    @classmethod
    def from_row(cls, row: Mapping[str, Any]) -> Self:
        """Deserialize a mysql-connector dictionary row into a RowModel instance.

        Automatically parses JSON string columns into Python lists/dicts when
        the target field expects a collection or mapping.
        """
        parsed: dict[str, Any] = dict(row)

        for key, val in parsed.items():
            if isinstance(val, str) and key in cls.model_fields:
                stripped = val.strip()
                if stripped.startswith(("{", "[")):
                    with contextlib.suppress(json.JSONDecodeError):
                        parsed[key] = json.loads(stripped)

        return cls.model_validate(parsed)


_http_url = TypeAdapter(HttpUrl)


def check_http_url(value: str | None) -> str | None:
    """Field validator ensuring a valid http(s) url"""
    if value is not None:
        _http_url.validate_python(value)
    return value
