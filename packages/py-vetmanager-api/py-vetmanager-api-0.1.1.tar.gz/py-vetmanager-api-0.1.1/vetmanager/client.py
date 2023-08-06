import requests

from vetmanager.domain import Domain

class WrongAuthentificationException(Exception):
    pass

class ExecutionException(Exception):
    pass

class VetmanagerClient:
    app_name: str
    domain: Domain
    def __init__(self, app_name: str, domain: Domain):
        self.app_name = app_name
        self.domain = domain

    def token(self, login: str, password: str) -> str:
        request_data = {
            'login': login,
            'password': password,
            'app_name': self.app_name
        }
        try :
            response = requests.post(self.domain.url() +  '/token_auth.php', data = request_data)
            response_json = response.json()
        except Exception:
            raise ExecutionException("Invalid response or server unavailable")

        if response.status_code == 401:
            raise WrongAuthentificationException(response_json['title'])
        if response.status_code == 500:
            raise ExecutionException(response_json['title'])
        return response_json['data']['token']


