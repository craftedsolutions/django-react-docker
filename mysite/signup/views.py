from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.core.mail import send_mail

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from signup.usecases.create_user import CreateUser
from signup.usecases.generate_token import GenerateToken
from signup.usecases.get_user_details import GetUserDetails

from signup.usecases.factory import UsecaseFactory

from signup.persistence.account_repo import AccountRepo

from signup.support.action_result_factory import of_success, of_failure, id
from signup.web.create_user_validator import CreateUserValidator
from signup.web.generate_token_validator import GetTokenValidator

from signup.web.deserializer import Deserializer

from signup.serializers import UserDetailsSerializer


def deserializationErrorResponse(errorMessage):
    response = JsonResponse({'error': "bad request body"})
    response.status_code = 400
    return response


def validationErrorResponse(errors):
    response = JsonResponse({'errors': errors})
    response.status_code = 400
    return response


def errorCreatingUserResponse(errorMessage):
    response = JsonResponse({'error': "failed to persist user"})
    response.status_code = 500
    return response


def userCreated(createdUser):
    confirmationCode = createdUser.registration.confirmation_code
    send_mail(
        'Subject here',
        'User was created and whatnot, need some sort of confirmation, you could use this code:\n\n\tCONFIRMATION CODE:' + confirmationCode,
        'from@example.com',
        ['to@example.com'],
        fail_silently=True,
    )
    response = JsonResponse({'key': 'success'})
    response.status_code = 201
    return response


@csrf_exempt
def create_user(request):
    if request.method != 'POST':
        response = JsonResponse({'error': "wrong method"})
        response.status_code = 405
        return response

    return Deserializer().attemptToDeserialize(
        request.body
    ).mapError(
        deserializationErrorResponse
    ).fmap(
        CreateUserValidator().is_valid
    ).mapError(
        validationErrorResponse
    ).fmap(
        CreateUser(user_persistence=UserRepo()).execute
    ).mapError(
        errorCreatingUserResponse
    ).ifSuccessOrElse(
        ifSuccess=userCreated,
        ifError=id,
    )


def errorGeneratingToken(errorMessage):
    response = JsonResponse(
        {'error': "failed to generate auth_token", 'message': errorMessage})
    response.status_code = 500
    return response


def tokenGenerated(token):
    return JsonResponse({'token': token, 'type': "Bearer"})


@csrf_exempt
def generate_token(request):
    if request.method != 'POST':
        response = JsonResponse({'error': 'wrong method'})
        response.status_code = 405
        return response

    return Deserializer().attemptToDeserialize(
        request.body
    ).mapError(
        deserializationErrorResponse
    ).fmap(
        GetTokenValidator().is_valid
    ).mapError(
        validationErrorResponse
    ).fmap(
        GenerateToken(user_persistence=AccountRepo()).execute
    ).mapError(
        errorGeneratingToken
    ).ifSuccessOrElse(
        ifSuccess=tokenGenerated,
        ifError=id,
    )


def emailConfirmed():
    return Response


@csrf_exempt
def confirm_email(request):
    if request.method != 'POST':
        response = JsonResponse({'error': 'wrong method'})
        response.status_code = 405
        return response

    return Deserializer().attemptToDeserialize(
        request.body
    ).mapError(
        deserializationErrorResponse
    ).fmap(
        ConfirmEmailValidator().is_valid
    ).mapError(
        validationErrorResponse
    ).fmap(
        ConfirmEmail(user_persistence=UserRepo).execute
    ).mapError(
        errorGeneratingToken
    ).ifSuccessOrElse(
        ifSuccess=emailConfirmed,
        ifError=id,
    )


def errorGettingUserDetails(message):
    return Response(
        data={'message': ['error getting user details', message]},
        status=status.HTTP_500_INTERNAL_SERVER_ERROR
    )

def serializeData(userDetails):
    serializer = UserDetailsSerializer(userDetails)
    return Response(serializer.data)

@api_view(["GET"])
def get_user_details(request):
    permission_classes = [IsAuthenticated]

    factory = UsecaseFactory()

    return of_success(
        request.user
    ).map(
        lambda user : user.id
    ).fmap(
        factory.user_details_usecase().execute
    ).mapError(
        errorGettingUserDetails
    ).ifSuccessOrElse(
        ifSuccess=serializeData,
        ifError=id,
    )
