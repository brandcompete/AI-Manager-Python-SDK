import requests, json, jwt

from collections import namedtuple
from typing import Any, NamedTuple, Optional
from brandcompete.core.util import Util
from brandcompete.core.classes import Route
class AccessToken(NamedTuple):
    """Represents an OAuth access token."""

    token: str
    refresh_token:str
    expires_on: int

AccessToken.token.__doc__ = """The token string."""
AccessToken.refresh_token.__doc__ = """The token need for refreshing current accestoken string."""
AccessToken.expires_on.__doc__ = """The token's expiration time in Unix time."""

class TokenCredential():

    def __init__(self, api_host_url:str, user_name:str, password:str, auto_refresh_token = True) -> None:
        self.auto_refresh_token = auto_refresh_token
        self.api_host = Util.validate_url(api_host_url)
        self.access = self.get_token(api_host_url=api_host_url, user_name=user_name, password=password)
        
        

    def get_token(cls, api_host_url:str, user_name:str, password:str) -> AccessToken:
        """Generate an AccessToken 

        Args:
            api_host_url (str): The API-Host example: https://aiman-api.brandcompete.com
            user_name (str): The Username to login
            password (str): The User related password

        Raises:
            Exception: Raise if login was not successfully

        Returns:
            AccessToken: AccessToken instance with expiration time in Unix time
        """
        
        data = {"userName": user_name, "userPassword": password}
        headers = {
                "accept": "application/json", 
                "Content-Type": "application/json"
                }
        base_url = Util.validate_url(api_host_url)
        url = f"{base_url}{Route.AUTH.value}"
        response = requests.post(url=url, headers=headers, json=data, allow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"[{response.status_code}] Reason: {response.reason}")
        
        return cls._to_access_token_object(response=response)
    
    @classmethod
    def refresh_access_token(cls) -> AccessToken:
        """Refreshing an existing AccessToken object

        Raises:
            Exception: Raise if refresh was not successfully

        Returns:
            AccessToken: AccessToken instance with expiration time in Unix time
        """
        
        data = {}
        response = requests.post(url=f"{cls.api_host}{Route.AUTH_REFRESH.value}", json=data, allow_redirects=True)
        if response.status_code != 200:
            raise Exception(f"[{response.status_code}] Reason: {response.reason}")
        
        cls.access = cls._to_access_token_object(response_content=response.content)
        return cls.access
        
    @classmethod
    def _to_access_token_object(cls, response:requests.Response ) -> AccessToken:
        """Warning: This method should not called externally
           Converts an api authentication response into an AccessToken instance

        Args:
            response (requests.Response): api authentication response

        Returns:
            AccessToken: AccessToken instance with expiration time in Unix time
        """
        content = json.loads(response.content.decode('utf-8')) 
        token = content['messageContent']['data']['access_token']
        refresh_token = content['messageContent']['data']['refresh_token']
        expires_on = int(jwt.decode(jwt=token, options={"verify_signature": False},algorithms=["HS256"])['exp'])
        return AccessToken(token=token, refresh_token=refresh_token, expires_on=expires_on)

__all__ = [
    "AccessToken",
    "TokenCredential",
]