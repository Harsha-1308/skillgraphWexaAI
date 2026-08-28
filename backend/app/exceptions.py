"""Custom application exceptions."""


class SkillGraphError(Exception):
    """Base exception for SkillGraph application errors."""


class DatabaseUnavailableError(SkillGraphError):
    """Raised when the graph database cannot be reached."""


class NotFoundError(SkillGraphError):
    """Raised when a requested resource does not exist."""

    def __init__(self, resource: str, resource_id: str):
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} with id '{resource_id}' not found.")


class ValidationError(SkillGraphError):
    """Raised when input validation fails."""
