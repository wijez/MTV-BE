import random
from datetime import timedelta

from django.conf import settings
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from MSRV.apps.utils.template_mail import TemplateMail
from MSRV.apps.utils.enum_type import TypeEmailEnum


def sent_mail_verification(user, type_mail, **kwargs):
    verify_code = get_random_string(length=8)
    user.verify_code = verify_code
    user.code_lifetime = timezone.now() + timedelta(minutes=10)
    user.save()
    message = ""
    template_mail = ""
    if type_mail == TypeEmailEnum.REGISTER:
        message = TemplateMail.CONTENT_MAIL_REGISTER_ACCOUNT(user.full_name, verify_code)
        template_mail = TemplateMail.SUBJECT_MAIL_REGISTER_ACCOUNT
    elif type_mail == TypeEmailEnum.RESET_PASSWORD:
        message = TemplateMail.CONTENT_MAIL_RESET_PASSWORD(user.full_name, verify_code)
        template_mail = TemplateMail.SUBJECT_MAIL_RESET_PASSWORD
    elif type_mail == TypeEmailEnum.REGISTER_FROM_ADMIN:
        password = kwargs.get("password", "Mật khẩu không có sẵn")
        message = TemplateMail.CONTENT_MAIL_REGISTER_FROM_ADMIN(user.email, verify_code,password)
    send_mail(
        template_mail,
        strip_tags(message),
        settings.EMAIL_HOST_USER,
        [user.email],
        html_message=message
    )
