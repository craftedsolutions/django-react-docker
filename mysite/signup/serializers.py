from signup.usecases.factory import UsecaseFactory
from djoser.serializers import UserSerializer
from django.contrib.auth import authenticate, get_user_model

from django.db import IntegrityError, transaction, DatabaseError

from rest_framework import serializers

from djoser.conf import settings
from djoser.serializers import TokenCreateSerializer, UserSerializer, UserCreatePasswordRetypeSerializer

from signup.models import EmailConfirmation, EmailConfirmationCode

User = get_user_model()


class CustomTokenCreateSerializer(TokenCreateSerializer):
    def validate(self, attrs):
        password = attrs.get("password")
        params = {settings.LOGIN_FIELD: attrs.get(settings.LOGIN_FIELD)}

        self.user = authenticate(
            request=self.context.get("request"),
            **params,
            password=password,
        )

        if not(self.user):
            self.user = User.objects.filter(**params).first()
            if self.user and not self.user.check_password(password):
                self.fail("invalid_credentials")

        if self.user:
            return attrs

        self.fail("invalid_credentials")


class CustomUserSerializer(UserSerializer):
    def update(self, instance, validated_data):
        print("Calling the custom: " + self.__class__.__name__)
        return super().update(instance, validated_data)


class CustomUserCreateSerializer(UserCreatePasswordRetypeSerializer):
    def perform_create(self, validated_data):
        validated_data['username'] = "default_username"

        def user_created(created_user):
            return created_user

        def user_create_failed():
            self.fail()

        account_repo = UsecaseFactory().get_account_repo()
        return account_repo.create_user(
            validated_data,
            success=user_created,
            failure=user_create_failed,
        )


class CustomActivationSerializer(serializers.Serializer):
    code = serializers.CharField()

    default_error_messages = {
        "invalid_code": "HARD_CODED_FOR_NOW",
    }

    def validate(self, attrs):
        attrs = super().validate(attrs)
        user = self.context["request"].user

        if not(user):
            self.fail("No authenticated user present")

        code = attrs["code"]
        if code == user.emailconfirmationcode.code:
            with transaction.atomic():
                emailconfirmation = user.emailconfirmation
                emailconfirmation.email_confirmed = True
                emailconfirmation.save()

            self.user = user  # to make the library view happy
            return attrs
        self.fail("invalid_code")


class UserDetailsSerializer(serializers.Serializer):
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    email_confirmed = serializers.BooleanField()
