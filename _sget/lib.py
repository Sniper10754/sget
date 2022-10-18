import sys
from typing import TextIO
from urllib.parse import urlparse

import requests

from .exceptions import DownloadException, MalformedURLException

def validate_url(x) -> bool:
    try:
        result = urlparse(x)
        return all([result.scheme, result.netloc])
    except:
        return False


def determine_url_protocol(url: str) -> str:
    """Gets url's protocol
    Just a wrapper of urllib.urlparse
    
    Args:
        url (str): The actual url

    Returns:
        str: the protocol
    """

    return urlparse(url).scheme

def determine_url_target(url: str) -> str:
    """Gets url's target
    Just a wrapper of urllib.urlparse

    Args:
        url (str): The actual url

    Returns:
        str: the protocol
    """
    
    return urlparse(url).netloc
    
def download(url, output: TextIO = sys.stdout, encoding="utf8") -> None:
    """Downloads from an url

    Args:
        url (str): The url to download from
        output (stream-like object, optional): A .write able object. Defaults to sys.stdout.
    """

    protocol = determine_url_protocol(url)
    
    if protocol == "https" or protocol == "http":
        response = download_http(url)
        output.write(response.decode(encoding=encoding))
    

    protocol = determine_url_protocol(url)


def download_http(url) -> bytes:
    
    response = requests.get(url)

    if not response.ok:
        raise DownloadException(
            "Something went wrong, response returned " + str(response.status_code)
        )
    else:
        return response.content
    
def download_ftp(url, credentials = ()) -> bytes:
    server = ftplib.FTP()
    server.connect('192.168.135.101', 5556)
    server.login(credentials[0], credentials[1])
