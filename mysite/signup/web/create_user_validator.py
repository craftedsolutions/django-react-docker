from signup.support.action_result_factory import of_success, of_failure

class CreateUserValidator(object):
    def is_valid(self, userData):
        errors = []

        if not('email' in userData):
            errors.append("[email] is required")
        if not('password' in userData):
            errors.append("[password] is required")
        if not('passwordConfirmation' in userData):
            errors.append("[passwordConfirmation] is required")
        if not('agreeToTerms' in userData):
            errors.append("[agreeToTerms] is required")

        if len(errors) > 0:
            return of_failure(failure_data=errors)

        if userData['password'] != userData['passwordConfirmation']:
            errors.append("[password] must match [passwordConfirmation]")
            return of_failure(failure_data=errors)
        if userData['agreeToTerms'] != True:
            errors.append("[agreeToTerms] must be true")
            return of_failure(failure_data=errors)

        return of_success(data=userData)