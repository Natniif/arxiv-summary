from bs4 import BeautifulSoup
import requests

def request_url(url: str): 
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		return response.content
	except requests.RequestException as e:
		print(f"Request failed: {e}")
		return ""

def create_topis_dict() -> dict:
	url = "https://arxiv.org"
	html_content = request_url(url)
	soup = BeautifulSoup(html_content, 'html.parser')

	paths = {} 
	content = soup.find('div', id='content')

	if not content: 
		return paths

	a_tags = content.find_all('a')
	
	for tag in a_tags:
		if 'id' in tag.attrs: 
			tag_id = tag.get_text(strip=True).replace(" ", "_").lower()
			tag_href = tag.get('href', '')
			# some paths for certain topics do not list the top papers
			if "/list/" in tag_href:
				paths[tag_id] = tag_href


	return paths

if __name__ == '__main__': 
	paths = create_topis_dict()
	for id, href in paths.items(): 
		print(f"ID: {id:50}, HREF: {href}")
