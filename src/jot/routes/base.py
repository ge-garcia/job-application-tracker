from pydantic import ValidationError


def format_validation_errors(exc: ValidationError) -> list[str]:
    """Flatten Pydantic ValidationError details into user-facing messages"""
    messages: list[str] = []
    for err in exc.errors():
        loc = ".".join(str(part) for part in err["loc"])
        msg = err["msg"]
        messages.append(f"{loc}: {msg}" if loc else msg)
    return messages
