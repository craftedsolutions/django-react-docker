from signup.support.action_result_factory import of_failure, of_success


class GenerateToken(object):
    def __init__(self, user_persistence):
        self.persistence = user_persistence

    def execute(self, userData):
        password = userData['password']
        email = userData['email']

        def ifFound(matchingUser):
            if matchingUser.check_password(password):
                return of_success('1234321')
            return of_failure("Password did not match")

        def ifNotFound():
            return of_failure('User not found')

        def ifError():
            return of_failure('Error')

        return self.persistence.get_user_by_email(
            success=ifFound,
            not_found=ifNotFound,
            error=ifError,
            email=email,
        )
