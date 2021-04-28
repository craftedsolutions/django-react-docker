from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.auth.models import User

class Registration(models.Model):

    class EmailVerification(models.TextChoices):
        PENDING = 'PENDING', _('Pending Verification')
        VERIFIED = 'VERIFIED', _('Email Verified')

    confirmation_code = models.CharField(max_length=8)
    registration_state = models.CharField(
        max_length=8,
        choices=EmailVerification.choices,
        default=EmailVerification.PENDING,
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def email_is_verified():
        return registration_state == EmailVerification.VERIFIED