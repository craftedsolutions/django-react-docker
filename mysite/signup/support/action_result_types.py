class TerminalFailedAction(object):
    def __init__(self, error_data):
        self.error_data = error_data
    def map(self, fun):
        return self

    def fmap(self, fun):
        return self

    def mapError(self, fun):
        return self

    def ifSuccessOrElse(self, ifSuccess, ifError):
        return ifError(self.error_data)


class FailedAction(object):
    def __init__(self, error_data):
        self.error_data = error_data

    def map(self, fun):
        return self

    def fmap(self, fun):
        return self

    def mapError(self, fun):
        return TerminalFailedAction(error_data=fun(self.error_data))

    def ifSuccessOrElse(self, ifSuccess, ifError):
        return ifError(self.error_data)


class SuccessfulAction(object):
    def __init__(self, data):
        self.data = data

    def map(self, fun):
        return SuccessfulAction(data=fun(self.data))

    def fmap(self, fun):
        return fun(self.data)

    def mapError(self, fun):
        return self

    def ifSuccessOrElse(self, ifSuccess, ifError):
        return ifSuccess(self.data)
