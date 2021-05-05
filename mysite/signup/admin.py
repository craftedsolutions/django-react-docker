from django.contrib import admin

from .models import CustomUser, EmailConfirmation, EmailConfirmationCode

admin.site.register(CustomUser)
admin.site.register(EmailConfirmation)
admin.site.register(EmailConfirmationCode)