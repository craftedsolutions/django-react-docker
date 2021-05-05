from django.db import transaction, DatabaseError

from signup.models import CustomUser, EmailConfirmation, EmailConfirmationCode


class AccountRepo(object):

    def __init__(self, token_generator):
        self.token_generator = token_generator

    def create_user(self, user_data, success, failure):
        try:
            with transaction.atomic():
                user_data['username'] = "default_username"
                user = CustomUser.objects.create_user(**user_data)

                code = self.token_generator()
                email_confirmation_code = EmailConfirmationCode(
                    user=user,
                    code=code
                )

                email_confirmation = EmailConfirmation(user=user)

                email_confirmation.save()
                email_confirmation_code.save()

                return success(user)
        except DatabaseError as dbError:
            print("Error creating user {0}".format(dbError))

        return failure()

    def get_user_by_email(email, success, not_found, error):
        try:
            user = User.objects.filter(email=email)
            if len(users) == 0:
                return not_found()

            if len(users) == 1:
                return success(users[0])
        except DatabaseError as dbError:
            print("Error finding user by email {0}".format(dbError))

        return error()

    def get_user_details(self, user_id, success, not_found, error):
        try:
            user = CustomUser.objects.get(pk=user_id)
            emailconfirmation = user.emailconfirmation

            return success({
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'email_confirmed': emailconfirmation.email_confirmed,
            })
        except CustomUser.DoesNotExist as e:
            return not_found()
        except DatabaseError as dbError:
            print("Error getting user details {0}".format(dbError))

        return error()
