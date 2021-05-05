from signup.support.action_result_factory import of_failure, of_success

class GetUserDetails(object):
    def __init__(self, repo):
        self.repo = repo

    def execute(self, user_id):
        def success(user_details):
            return of_success(user_details)

        def not_found():
            return of_failure("Failed to find user details")

        def error(message):
            return of_failure(message)

        return self.repo.get_user_details(
            user_id,
            success=success,
            not_found=not_found,
            error=error
        )
