from django.contrib.auth.tokens import default_token_generator
from templated_mail.mail import BaseEmailMessage

from djoser.conf import settings
from djoser.email import ActivationEmail

class CustomActivationEmail(BaseEmailMessage):
    template_name = "signup/email/activation.html"

    def get_context_data(self):
        # ActivationEmail can be deleted
        context = super().get_context_data()

        user = context.get("user")
        context["confirmation_token"] = user.emailconfirmationcode.code

        return context