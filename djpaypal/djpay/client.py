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
            response.raise_for_status()

        except requests.exceptions.Timeout as e:
            return f"Timed Out {e}"
        except requests.exceptions.ConnectionError as e:
            return f"Connection Error {e}"
        except requests.exceptions.HTTPError as e:
            return f"HttpError raised {e}"
        else:
            return response
