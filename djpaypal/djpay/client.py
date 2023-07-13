import requests
from dataclasses import dataclass
import json


@dataclass
class AuthorizationlAPI:
    api_client: str
    api_secret: str

    def post(self, data, base_url, timeout=10):
        try:
            response = requests.post(
                base_url, data, auth=(self.api_client, self.api_secret), timeout=timeout
            )
        except requests.exceptions.Timeout:
            raise "Request timed out."
        except requests.exceptions.RequestException as e:
            raise f"An error occurred during the request: {e}"

        res_data = json.loads(response.text)
        return res_data
