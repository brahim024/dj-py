import requests
from dataclasses import dataclass
from abc import ABC, abstractclassmethod


class PaypalClient(ABC):
    @abstractclassmethod
    def post():
        pass


@dataclass
class AuthorizationAPI(PaypalClient):
    api_client: str
    api_secret: str

    def post(self, base_url, data, *args, **kwargs):
        try:
            response = requests.post(
                base_url,
                data,
                auth=(self.api_client, self.api_secret),
                timeout=kwargs.get("timeout", 10),
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
