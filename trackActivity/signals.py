from django.contrib.auth.signals import user_logged_in, user_login_failed
from django.dispatch import receiver

from .models import ActivityLog,  LOGIN, LOGIN_FAILED


def get_client_ip(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    return (
        x_forwarded_for.split(",")[0]
        if x_forwarded_for
        else request.META.get("REMOTE_ADDR")
    )


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    message = f"{user.email} is logged in with ip:{get_client_ip(request)}"
    ActivityLog.objects.create(actor=user, action_type=LOGIN, remarks=message, school = user.school)


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    message = f"Login Attempt Failed for email {credentials.get('email')} with ip: {get_client_ip(request)}"
    ActivityLog.objects.create(action_type=LOGIN_FAILED, remarks=message)