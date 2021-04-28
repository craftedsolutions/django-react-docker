from signup.support.action_result_factory import of_success, of_failure

class GetTokenValidator(object):
    def is_valid(self, data):
        errors = []

        if not('email' in data):
            errors.append("[email] is required")
        if not('password' in data):
            errors.append("[password] is required")

        if len(errors) > 0:
            return of_failure(failure_data=errors)

        return of_success(data=data)