from urllib.parse import urlparse
import time, os


class Util:

    @classmethod
    def validate_url(cls, url:str) -> str:
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
            raise ValueError("Invalid URL: {}".format(url))
        
        return url

    @classmethod
    def get_current_unix_time(cls) -> int:
        return time.time()
    
    @classmethod
    def is_token_expired(cls, expire_unix_time: int) -> bool:
        return cls.get_current_unix_time() >= expire_unix_time
    
    @classmethod
    def get_file_name(cls, file_path:str) -> str:
        return os.path.basename(file_path)

__all__ = [
    "Util"
]