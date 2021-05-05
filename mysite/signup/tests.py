from rest_framework.test import APITestCase
from rest_framework import status
from django.core import mail

from signup.support.action_result_factory import of_failure, of_success, id
from unittest.mock import patch

import json
from json import JSONDecodeError


def test_confirmation_code(code):
    def provideCode():
        print("Should be calling the test provider...")
        return code
    return provideCode


def attemptToParse(maybeJsonString):
    try:
        return of_success(json.loads(maybeJsonString))
    except JSONDecodeError as e:
        return of_failure("{0}".format(e))


def validBody(
    email="ok@email.com",
    password="pre77yg00d",
    last_name="last name",
    first_name="first name"
):
    return {
        'email': email,
        'password': password,
        're_password': password,
        'first_name': first_name,
        'last_name': last_name,
        'licenseStatus': "NOT_LICENSED",
        'agreeToTerms': True,
    }


def extract_auth_token(test, content):
    contentJson = json.loads(str(content, encoding='utf8'))
    test.assertIn("auth_token", contentJson)

    return contentJson["auth_token"]


class SignupApiTests(APITestCase):

    register_url = "/signup/api/users/"
    login_url = "/signup/api/token/login/"
    activation_url = "/signup/api/users/activation/"
    user_details_url = "/signup/api/user_details/"

    @patch("signup.usecases.factory.generate_code", test_confirmation_code("TEST_CODE")) # we should talk about this
    def test_create_user_success(self):
        email = "fancy@mail.com"
        password = "$ecre711"
        first_name = "a pretty good first name"
        last_name = "also pretty good as a last name"

        body = validBody(
            email=email,
            password=password,
            last_name=last_name,
            first_name=first_name,
        )
        user_creation_response = self.client.post(
            self.register_url,
            data=body,
            format="json"
        )

        self.assertIs(
            user_creation_response.status_code,
            status.HTTP_201_CREATED
        )

        login_response = self.client.post(
            self.login_url,
            data={'email': email, 'password': password},
            format="json"
        )

        self.assertIs(login_response.status_code, status.HTTP_200_OK)

        auth_token = extract_auth_token(self, login_response.content)

        self.assertIsNotNone(auth_token)
        self.assertIsNot(auth_token, "")

        self.assertEqual(len(mail.outbox), 1)
        email_body = mail.outbox[0].body
        confirmation_code = "TEST_CODE"

        self.assertIn(confirmation_code, email_body)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        confirmationResponse = self.client.post(
            self.activation_url,
            data={"code": confirmation_code},
            format="json",
        )

        self.assertIs(
            confirmationResponse.status_code,
            status.HTTP_204_NO_CONTENT
        )

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        user_details_response = self.client.get(self.user_details_url)

        self.assertIs(
            user_details_response.status_code,
            status.HTTP_200_OK
        )

        def failedToParse(errorMessage):
            self.fail("Failed to parse user_details: " + errorMessage)

        self.assertJSONEqual(user_details_response.content, {
            "email": email,
            "last_name": last_name,
            "first_name": first_name,
            "email_confirmed": True,
        })

    def test_user_confirmation_status_included_in_get_user_response(self):
        email = "fancy@mail.com"
        password = "$ecre711"
        first_name = "a pretty good first name"
        last_name = "also pretty good as a last name"

        body = validBody(
            email=email,
            password=password,
            last_name=last_name,
            first_name=first_name,
        )
        user_creation_response = self.client.post(
            self.register_url,
            data=body,
            format="json"
        )

        self.assertIs(
            user_creation_response.status_code,
            status.HTTP_201_CREATED
        )

        login_response = self.client.post(
            self.login_url,
            data={'email': email, 'password': password},
            format="json"
        )

        auth_token = extract_auth_token(self, login_response.content)

        self.client.credentials(HTTP_AUTHORIZATION='Token ' + auth_token)
        user_details_response = self.client.get(self.user_details_url)

        self.assertIs(
            user_details_response.status_code,
            status.HTTP_200_OK
        )

        def failedToParse(errorMessage):
            self.fail("Failed to parse user_details: " + errorMessage)

        self.assertJSONEqual(user_details_response.content, {
            "email": email,
            "last_name": last_name,
            "first_name": first_name,
            "email_confirmed": False,
        })

    def test_email_must_be_unique(self):
        email = "repeaty@again.com"
        password1 = "at_least_8_chars"
        password2 = "also_likely_over_8_chars"

        body1 = validBody(email=email, password=password1)

        self.client.post(self.register_url, data=body1, format="json")

        body2 = validBody(email=email, password=password2)
        duplicate_email_response = self.client.post(
            self.register_url, data=body2, format="json")

        self.assertEquals(
            duplicate_email_response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

        def invalidResponseBody(message):
            self.fail("Invalid reponse body, unable to parse as json: " + message)

        error_string = duplicate_email_response.content
        error_json = attemptToParse(error_string).ifSuccessOrElse(
            ifSuccess=id,
            ifError=invalidResponseBody
        )

        self.assertIn("email", error_json)

        email_errors = error_json["email"]
        self.assertEqual(len(email_errors), 1)
        self.assertEqual(
            email_errors[0], "user with this email already exists.")
