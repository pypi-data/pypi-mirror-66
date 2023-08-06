import unittest
from unittest import mock
from vetmanager.domain import DomainTest
from vetmanager.client \
    import VetmanagerClient, ExecutionException, WrongAuthentificationException


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


class TestClient(unittest.TestCase):
    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_success(self, mock):
        domain = DomainTest('tests')
        client = VetmanagerClient('test_app', domain)
        mock.return_value = MockResponse({
            "status": 200,
            "title": "Authorization completed.",
            "detail": "Авторизация выполнена.",
            "data": {
                "service": "test_app",
                "token": 'test_token',
                'user_id': 1,
            }
        }, 200)
        self.assertEqual(client.token('login', 'password'), 'test_token')

    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_wrong_password(self, mock):
        domain = DomainTest('tests')
        client = VetmanagerClient('test_app', domain)
        mock.return_value = MockResponse({
            "status": 401,
            "title":  "Wrong authentification.",
            "detail": "Error Message"
        }, 401)
        with self.assertRaises(WrongAuthentificationException):
            client.token('login', 'password')

    @mock.patch('vetmanager.client.requests.post')
    def test_vetmanager_client_auth_execution_problem(self, mock):
        domain = DomainTest('tests')
        client = VetmanagerClient('test_app', domain)
        mock.return_value = MockResponse({
            "status": 500,
            "title":  "Wrong authentification.",
            "detail": "Error Message"
        }, 500)
        with self.assertRaises(ExecutionException):
            client.token('login', 'password')


if __name__ == '__main__':
    unittest.main()
