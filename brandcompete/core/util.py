"""Module providing some utility or helper functions"""
import time
import os
from urllib.parse import urlparse
from brandcompete.core.classes import Loader

class Util:
    """Represents a Utility Class"""

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
            if not cls.check_is_url(url):
                if check_only is True:
                    return False
                return url
            if not url.lower().startswith('http'):
                url = "https://" + url
            if url.lower().startswith("http://"):
                url = url.replace("http://", "https://")
            if url.lower().endswith("/"):
                url = url[:-1]
        except AttributeError as e:
            raise AttributeError("url must be a string.") from e
        parsed_url = urlparse(url.rstrip('/'))
        if not parsed_url.netloc:
            if check_only is True:
                return False
            raise ValueError(f"Invalid URL: {url}")

        if check_only is True:
            return True
        return url

    @classmethod
    def check_is_url(cls, value:str) ->bool:
        """Check if given value is a url or not

        Args:
            value (str): value

        Returns:
            bool: url or not
        """
        if value.lower().startswith('http://'):
            return True
        if value.lower().startswith('https://'):
            return True
        if value.lower().startswith('www.'):
            return True
        return False

    @classmethod
    def get_current_unix_time(cls) -> int:
        """Get the current unix timestamp

        Returns:
            int: unix time
        """
        return time.time()

    @classmethod
    def is_token_expired(cls, expire_unix_time: int) -> bool:
        """Checks whether the token has expired

        Args:
            expire_unix_time (int): expire_unix_time

        Returns:
            bool: Is expired (true or false)
        """
        return cls.get_current_unix_time() >= expire_unix_time

    @classmethod
    def get_file_name(cls, file_path:str) -> str:
        """Returns the final component of a pathname"""
        return os.path.basename(file_path)

    @classmethod
    def get_file_name_and_ext(cls, file_path:str) -> tuple:
        """Get the filename and extension from a given path

        Args:
            file_path (str): file path (absolute or relative)

        Returns:
            tuple: filename and extension
        """
        filename, file_extension = os.path.splitext(file_path)
        filename = cls.get_file_name(file_path=file_path)
        return filename, file_extension.replace(".","")

    @classmethod
    def get_loader_by_ext(cls, file_ext:str) -> tuple:
        """Get a specific file content loader by file extension

        Args:
            file_ext (str): file extension

        Returns:
            tuple: loader and mime type
        """
        file_ext = file_ext.lower()
        if file_ext == "pdf":
            return Loader.PDF, "application/pdf"
        if file_ext == "csv":
            return Loader.CSV, "application/csv"
        if file_ext == "xlsx":
            return Loader.EXCEL, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        if file_ext == "docx":
            return Loader.DOCX, ""
        if file_ext in {"png", "tif", "jpeg", "jpg"}:
            return Loader.IMAGE, f"image/{file_ext}"
        return None

__all__ = [
    "Util"
]
