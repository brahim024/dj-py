import requests
from dataclasses import dataclass


@dataclass
class AuthorizationAPI:
    api_client: str
    api_secret: str

    def post(self, data, base_url=None, timeout=10):
        try:
            response = requests.post(
                base_url, data, auth=(self.api_client, self.api_secret), timeout=timeout
            )
        except TypeError as t_err:
            raise f"An error occurred during the request: {t_err}"
        except requests.exceptions.RequestException as e:
            raise f"An error occurred during the request: {e}"
        return response
