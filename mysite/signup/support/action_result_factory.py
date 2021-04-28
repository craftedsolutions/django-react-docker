from signup.support.action_result_types import SuccessfulAction, FailedAction

def of_success(data):
    return SuccessfulAction(data=data)

def of_failure(failure_data):
    return FailedAction(error_data=failure_data)

def id(arg):
    return arg