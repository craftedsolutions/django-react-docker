from signup.support.action_result_factory import of_success, of_failure

from json.decoder import JSONDecodeError

import json

class Deserializer(object):
    def __init__(self):
        self

    def attemptToDeserialize(self, raw_body):
        try:
            body_string = raw_body.decode('utf-8')

            return of_success(json.loads(body_string))
        except JSONDecodeError as e:
            print("Error {0}".format(e))

        return of_failure(failure_data="Failed to deserialize body")
