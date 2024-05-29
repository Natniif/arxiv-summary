import requests
from typing import Union

REQUEST_TIMEOUT = 2

def request_url(url: str) -> Union[str, bytes]: 
	try:
		response = requests.get(url, timeout=REQUEST_TIMEOUT)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		return response.content
	except requests.RequestException as e:
		print(f"Request failed: {e}")
		return ""