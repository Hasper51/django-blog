import yagmail
from celery import shared_task


@shared_task
def send_email_yandex(smtp_server: str, smtp_port: int, user_email: str, user_password: str, recipient_email: str, subject: str, body: str):
    try:
        yag = yagmail.SMTP(
            user=user_email,
            password=user_password,
            host=smtp_server,
            port=smtp_port,
        )

        yag.send(
            to=recipient_email,
            subject=subject,
            contents=body,
        )
        print("Email отправлен успешно.")
    except Exception as e:
        print(f"Ошибка отправки email: {e}")
