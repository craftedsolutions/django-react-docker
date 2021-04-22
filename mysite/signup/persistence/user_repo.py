from django.contrib.auth.models import User

class UserRepo(object):
    def __init__(self):
        self

    def save(self, user_data):
        user = User.objects.create_user(user_data.name, email=user_data.email, password=user_data.password, is_active=user_data.is_active)
        return True