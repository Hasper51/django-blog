from ninja import Schema


class UserFilters(Schema):
    search: str | None = None
