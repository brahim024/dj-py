import requests
from dataclasses import dataclass
import json
from requests.exceptions import HTTPError

@dataclass
class AuthorizationAPI:
    api_client: str
    api_secret: str

    def post(self, data, base_url, timeout=10):
        try:
            response = requests.post(
                base_url, data, auth=(self.api_client, self.api_secret), timeout=timeout
            )
        except requests.exceptions.Timeout as err:
            raise err

        except requests.exceptions.RequestException as e:
            raise f"An error occurred during the request: {e}"


        return response
