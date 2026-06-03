from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from materials.models import Course, Subscription


@shared_task
def send_course_update_email(course_id: int):
    """
    Асинхронная задача Celery для отправки email-уведомлений подписчикам (Задание 2).
    """
    try:
        course = Course.objects.get(pk=course_id)
    except Course.DoesNotExist:
        return f"Курс с ID {course_id} не найден."

    # Отбираем подписки на этот курс
    subscriptions = Subscription.objects.filter(course=course).select_related("user")
    recipient_list = [sub.user.email for sub in subscriptions if sub.user.email]

    if not recipient_list:
        return f"Нет активных подписчиков для курса '{course.name}'."

    subject = f"Обновление материалов курса: {course.name}"
    message = f"Здравствуйте!\n\nВ курсе '{course.name}' произошли изменения или добавились новые уроки. Заходите на платформу, чтобы продолжить обучение!"

    # Отправляем фоновое письмо (Задание 2)
    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=recipient_list,
        fail_silently=False,
    )

    return f"Уведомления об обновлении курса '{course.name}' успешно отправлены на {len(recipient_list)} адресов."
