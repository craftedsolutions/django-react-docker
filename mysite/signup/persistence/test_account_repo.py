from django.test import TestCase

import uuid

from signup.support.action_result_factory import id
from signup.persistence.account_repo import AccountRepo


def test_token_generator():
    return "11111ß"


class AccountRepoTests(TestCase):
    def should_not_be_called(self, name):
        return lambda: self.fail("[" + name + "]" + " should not have been called")

    def test_user_can_be_created_and_retrieved(self):
        repo = AccountRepo(token_generator=test_token_generator)

        def create_user_success(created_user):
            return created_user

        user_data = {
            'email': "a@b.com",
            'first_name': "fn",
            'last_name': "ln",
            'password': "over_8_characters",
        }
        created_user = repo.create_user(
            user_data=user_data,
            failure=self.should_not_be_called("create_user_failure"),
            success=create_user_success,
        )

        self.assertIsNotNone(created_user)

        actual_user_details = repo.get_user_details(
            created_user.id,
            success=id,
            not_found=self.should_not_be_called("get_user_details_not_found"),
            error=self.should_not_be_called("get_user_details_error"),
        )

        self.assertEqual(actual_user_details['first_name'], "fn")
        self.assertEqual(actual_user_details['last_name'], "ln")
        self.assertEqual(actual_user_details['email'], "a@b.com")
        self.assertEqual(actual_user_details['email_confirmed'], False)

    def test_get_user_details_for_non_existing_user_triggers_not_found_callback(self):
        repo = AccountRepo(token_generator=test_token_generator)

        not_existing_user = 77
        expected_result = uuid.uuid4()

        def not_found():
            return expected_result

        actual_result = repo.get_user_details(
            not_existing_user,
            success=self.should_not_be_called("get_user_details success"),
            not_found=not_found,
            error=self.should_not_be_called("get_user_details error"),
        )

        self.assertEqual(actual_result, expected_result)
