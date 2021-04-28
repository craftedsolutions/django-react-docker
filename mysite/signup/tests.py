from django.test import TestCase
from django.core import mail

from unittest.mock import patch

import json


class SignupApiTests(TestCase):

    def test_create_user_success(self):
        email = "fancy@mail.com"
        password = "$ecre7"

        body = {
            'email': email,
            'password': password,
            'passwordConfirmation': password,
            'firstName': "first name",
            'lastName': "last name",
            'licenseStatus': "NOT_LICENSED",
            'agreeToTerms': True,
        }
        response = self.client.post(
            "/signup/user/", data=json.dumps(body), content_type="application/json")

        self.assertIs(response.status_code, 201)

        response = self.client.post("/signup/auth_token/", data=json.dumps(
            {'email': email, 'password': password}), content_type="application/json")

        self.assertIs(response.status_code, 200)

        contentJson = json.loads(str(response.content, encoding='utf8'))

        self.assertIn("token", contentJson)
        self.assertIn("type", contentJson)
        self.assertEqual(contentJson["type"], "Bearer")

        self.assertEqual(len(mail.outbox), 1)
        print(mail.outbox[0].body)

    def test_create_user_wrong_method_returns_405(self):
        unsupportedMethods = [
            "PATCH",
            "DELETE",
            "HEAD",
            "GET",
            "OPTIONS",
            "TRACE"
        ]
        for method in unsupportedMethods:
            response = self.client.generic(
                method, "/signup/user/", self.validBody())
            self.assertEqual(response.status_code, 405)

    def test_create_user_non_json_body_returns_400(self):
        response = self.client.post(
            "/signup/user/", data="some-non-json-string }{", content_type="application/json")

        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_json_attributes_returns_400(self):
        requestBody = self.validBody()
        del requestBody['email']

        response = self.client.post(
            "/signup/user/", data=json.dumps(requestBody), content_type="application/json")

        self.assertEquals(response.status_code, 400)

        errorJson = json.loads(response.content)
        self.assertIn("errors", errorJson)

    def validBody(self, email="ok@email.com", password="pre77yg00d"):
        return {
            'email': email,
            'password': password,
            'passwordConfirmation': password,
            'firstName': "first name",
            'lastName': "last name",
            'licenseStatus': "NOT_LICENSED",
            'agreeToTerms': True,
        }
