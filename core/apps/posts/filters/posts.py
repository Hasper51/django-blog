from dataclasses import dataclass


@dataclass(frozen=True)
class PostFilters:
    search: str | None = None
