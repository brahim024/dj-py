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
        
        except Exception as e:
            raise   
            
        return response
