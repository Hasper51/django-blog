from typing import List

from ninja import Router

from core.api.v1.notifications.schemas import NotificationOutSchema
from core.api.v1.users.handlers.auth import AuthBearer
from core.apps.notifications.services.notification import BaseNotificationService
from core.project.containers import get_container


router = Router(tags=['Notifications'], auth=AuthBearer())


@router.get("/notifications/", response=List[NotificationOutSchema])
def get_notifications(request):
    container = get_container()
    service = container.resolve(BaseNotificationService)
    notifications = service.get_user_notifications(request.user.id)
    return [NotificationOutSchema.from_orm(notification) for notification in notifications]


@router.post("/notifications/{notification_id}/read/")
def mark_notification_as_read(request, notification_id: int):
    container = get_container()
    service = container.resolve(BaseNotificationService)
    service.mark_as_read(notification_id)
    return {"success": True}
