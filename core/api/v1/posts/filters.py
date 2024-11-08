from ninja import Schema


class PostFilters(Schema):
    search: str | None = None
