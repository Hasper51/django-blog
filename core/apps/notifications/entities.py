from dataclasses import (
    dataclass,
    field,
)
from datetime import datetime
from typing import Optional


@dataclass
class Notification:
    id: Optional[int] | None = field(default=None, kw_only=True) # noqa
    recipient_id: int
    actor_id: int
    notification_type: str
    target_id: int
    target_type: str
    is_read: bool
    created_at: datetime = field(default_factory=datetime.now)
