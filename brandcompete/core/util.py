from typing import Optional
from urllib.parse import urlparse
import time, os

from brandcompete.core.classes import Loader
from brandcompete.core.credentials import TokenCredential


class Util:

    @classmethod
    def validate_url(cls, url:str,check_only = False):
        """Validate and parse an url

        Args:
            url (str): url

        Raises:
            ValueError: If url is not type of string
            ValueError: If url couldnt parsed properly

        Returns:
            str: Parsed and proper formated url
        """
        try:
            if not url.lower().startswith('http'):
                url = "https://" + url
            if url.lower().startswith("http://"):
                url = url.replace("http://", "https://")
            if url.lower().endswith("/"):
                url = url[:-1]
        except AttributeError:
            raise ValueError("url must be a string.")
        parsed_url = urlparse(url.rstrip('/'))
        if not parsed_url.netloc:
            if check_only == True:
                return False
            raise ValueError("Invalid URL: {}".format(url))
        
        if check_only == True:
            return True
        return url

    @classmethod
    def get_current_unix_time(cls) -> int:
        """Get the current unix timestamp

        Returns:
            int: unix time
        """
        return time.time()
    
    @classmethod
    def is_token_expired(cls, token_credential: TokenCredential) -> bool:
        """Checks whether the token has expired

        Args:
            token (TokenCredential): Instance of TokenCredentials ()

        Returns:
            bool: Is expired (true or false)
        """
        return cls.get_current_unix_time() >= token_credential.access.expires_on
    
    @classmethod
    def get_file_name(cls, file_path:str) -> str:
        """Returns the final component of a pathname"""
        return os.path.basename(file_path)
    
    @classmethod
    def get_file_name_and_ext(cls, file_path:str) -> tuple:
       
        filename, file_extension = os.path.splitext(file_path)
        return cls.get_file_name(file_path=file_path), file_extension.replace(".","")

    @classmethod
    def get_loader_by_ext(cls, file_ext:str) -> tuple:
        
        if file_ext == "pdf":
            return Loader.PDF, "application/pdf"
        if file_ext == "csv":
            return Loader.CSV, "application/csv"
        if file_ext == "xlsx":
            return Loader.EXCEL, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if file_ext == "docx":
            return Loader.DOCX, ""
        if file_ext == "png" or file_ext == "tif" or file_ext == "jpeg" or file_ext == "jpg":
            return Loader.IMAGE, f"image/{file_ext}", 
        return None

__all__ = [
    "Util"
]
