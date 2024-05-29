from bs4 import BeautifulSoup
import requests

'''
The only reason I am keeping this file is for example if the html for arxiv changes for some reason
'''

def request_url(url: str) : 
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		return response.content
	except requests.RequestException as e:
		print(f"Request failed: {e}")
		return ""

def getInfo() -> None:
	url = "https://arxiv.org/list/cs.AI/recent"
	html_content = request_url(url)

	soup = BeautifulSoup(html_content, 'html.parser')

	if soup:
		return soup.prettify()

if __name__ == "__main__": 
	soup = getInfo()

	with open('test.html', 'w') as w: 
		w.write(soup)