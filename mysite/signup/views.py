from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from signup.usecases.create_user import CreateUser
from signup.usecases.generate_token import GenerateToken

from signup.persistence.user_repo import UserRepo

from django.core.mail import send_mail

from signup.support.action_result_factory import of_success, of_failure, id
from signup.web.create_user_validator import CreateUserValidator
from signup.web.generate_token_validator import GetTokenValidator

from signup.web.deserializer import Deserializer


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
    response = JsonResponse({'error': "failed to generate auth_token", 'message': errorMessage})
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
        GenerateToken(user_persistence=UserRepo).execute
    ).mapError(
        errorGeneratingToken
    ).ifSuccessOrElse(
        ifSuccess=tokenGenerated,
        ifError=id,
    )

def emailConfirmed():
    return JsonResponse({'message': "success"})

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