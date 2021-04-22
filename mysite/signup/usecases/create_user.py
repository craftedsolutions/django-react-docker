class CreateUser(object):
    def __init__(self, data, user_persistence):
        self.data = data
        self.persistence = user_persistence

    def execute(self, responseHandler):
        success = self.persistence.save(self.data)
        if success:
            return responseHandler.success()
        else:
            return responseHandler.failure()
