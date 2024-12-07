from datetime import datetime

from ninja import Schema


class NotificationOutSchema(Schema):
    id: int # noqa
    recipient_id: int
    actor_id: int
    notification_type: str
    target_id: int
    target_type: str
    is_read: bool
    created_at: datetime
