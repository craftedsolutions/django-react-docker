from django.contrib.auth.models import User

from signup.models import Registration

from django.db import transaction, DatabaseError


class UserRepo(object):
    def create_user(self, user_data, success, failure):
        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    username=user_data['firstName'],
                    email=user_data['email'],
                    password=user_data['password'],
                    is_active=False,
                )
                Registration.objects.create(
                    confirmation_code="11112222",
                    user=user,
                )

            return success(user)
        except DatabaseError as dbError:
            print("Error saving a new user {0}".format(dbError))
            return failure()

    def get_user_by_email(email, success, not_found, error):
        try:
            users = User.objects.filter(email=email)
            if len(users) == 0:
                return not_found()

            if len(users) == 1:
                return success(users[0])
        except DatabaseError as dbError:
            print("Error finding user by email {0}".format(dbError))

        return error()
