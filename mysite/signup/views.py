from django.http import JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

from signup.usecases.create_user import CreateUser
from signup.persistence.user_repo import UserRepo

import json

def index(request):
    print(request)
    return JsonResponse({
        'key': 'friendly value!'
    })

def blah(request):
    print(request)
    return JsonResponse({
        'key': 'real-good data!'
    })

@csrf_exempt
def register(request):
    if request.method == 'POST':
        body_string = request.body.decode('utf-8')
        print("Body -> " + body_string)

        user_data = json.loads(body_string)
        print(user_data)

        usecase = CreateUser(
            user_data,
            UserRepo()
        )
        return usecase.execute(CreateUserResponder())

    return JsonResponse({
        'key': 'woops :('
    })

class CreateUserResponder(object):
    def __init__(self):
        self
    def success(self):
        return JsonResponse({
            'key': 'success'
        })
    def failure(self):
        return JsonResponse({
            'key': 'failure'
        })