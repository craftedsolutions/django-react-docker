from signup.support.action_result_factory import of_success, of_failure


class CreateUser(object):
    def __init__(self, user_persistence):
        self.persistence = user_persistence

    def execute(self, user_data):
        def saveSuccess(savedUser):
            return of_success(savedUser)
        def saveFailure(error):
            return of_failure(error)

        return self.persistence.create_user(
            user_data,
            success=saveSuccess,
            failure=saveFailure,
        )
