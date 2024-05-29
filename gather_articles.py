from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Union
from bs4 import BeautifulSoup
import requests
import webbrowser
import argparse
from scripts.get_paths import *

BASE_URL = "https://arxiv.org"
REQUEST_TIMEOUT = 2

# ANSI escape codes for colors
class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'

@dataclass
class Paper:
	title: str = ""
	authors: List[str] = field(default_factory=list)
	pdf_link: str = ""
	subjects: List[str] = field(default_factory=list)
	abstract: str = ""
	id: int = 0

	def __repr__(self) -> str:
		escape_mask = '\033]8;{};{}\033\\{}\033]8;;\033\\'
		if len(self.abstract) != 0:
			return (
				f"\n"
				f"\n"
				f"------------------------[{self.id}]------------------------"
				f"\n"
				f"{Color.RED}{Color.UNDERLINE}{Color.BOLD}Title:{Color.END} {self.title}\n"
				f"{Color.CYAN}{Color.UNDERLINE}{Color.BOLD}Authors:{Color.END} {self.authors}\n"
				f"{Color.YELLOW}{Color.UNDERLINE}{Color.BOLD}subjects:{Color.END} {', '.join(self.subjects)}"
				f"{Color.PURPLE}{Color.UNDERLINE}{Color.BOLD}PDF Link:{Color.END} {self.pdf_link}\n"
				f"{Color.GREEN}{Color.UNDERLINE}{Color.BOLD}Abstract:{Color.END}\n \t{self.abstract}\n"
				f"------------------------[{self.id}]------------------------"
				f"\n")
		else: 
			return (
				f"\n"
				f"\n"
				f"------------------------[{self.id}]------------------------"
				f"\n"
				f"{Color.RED}{Color.UNDERLINE}{Color.BOLD}Title{Color.RED}:{Color.END} {self.title}\n"
				f"{Color.CYAN}{Color.UNDERLINE}{Color.BOLD}Authors{Color.CYAN}:{Color.END} {self.authors}\n"
				f"{Color.YELLOW}{Color.UNDERLINE}{Color.BOLD}subjects:{Color.YELLOW}{Color.END} {', '.join(self.subjects)}\n"
				f"{Color.PURPLE}{Color.UNDERLINE}{Color.BOLD}PDF Link{Color.PURPLE}:{Color.END} {self.pdf_link}\n"
				f"------------------------[{self.id}]------------------------"
				f"\n")

	def open_pdf(self) -> None: 
		# TODO add safety checks here
		webbrowser.open(self.pdf_link)

def request_url(url: str) -> Union[str, bytes]: 
	try:
		response = requests.get(url, timeout=REQUEST_TIMEOUT)
		response.raise_for_status()  # Raise an HTTPError for bad responses
		return response.content
	except requests.RequestException as e:
		print(f"Request failed: {e}")
		return ""

def getInfo(topic_url: str, abstract: bool =True, max_papers: int =25, ) -> None:
	# TODO: add support for other links
	url = BASE_URL + topic_url
	html_content = request_url(url)

	soup = BeautifulSoup(html_content, 'html.parser')

	if soup: 
		dl_tag = soup.find('dl', id='articles')
		if dl_tag: 
			article_list = parse_articles(dl_tag, abstract, max_papers)
		else: 
			print("Error: Could not find dl tag with articles.")

	for i in article_list: 
		print(i)

def extract_abstract(abstract_link: str)-> str: 
	html_content = request_url(abstract_link)
	soup = BeautifulSoup(html_content, 'html.parser')

	blockquote = soup.find('blockquote', class_='abstract mathjax')
	if not blockquote:
		return ""

	abstract_span = blockquote.find('span', class_="descriptor")
	if not abstract_span or not abstract_span.next_sibling:
		return ""

	abstract_text = abstract_span.next_sibling.strip(' "')

	return abstract_text

def parse_articles(dl_tag: BeautifulSoup, abstract: bool, max_papers: int)-> List[Paper]: 
	# links for each article inside the <dt> header
	# the meta information like title and authors is inside the <dd> <div class="meta"> tag

	article_list: List[Paper] = []

	dt_tags = dl_tag.find_all('dt')
	dd_tags = dl_tag.find_all('dd')

	iter = 1
	for dt, dd in zip(dt_tags, dd_tags):
		# links 
		paper = Paper()
		paper.id = iter
		pdf_link = dt.find('a', title="Download PDF")['href'] if dt.find('a', title='Download PDF') else ''
		paper.pdf_link = BASE_URL + pdf_link 

		if abstract == True:
			abstract_link = BASE_URL + dt.find('a', title='Abstract')['href']
			if abstract_link: 
				paper.abstract = extract_abstract(abstract_link)

		meta_div = dd.find('div', class_='meta')
		if meta_div: 

			title_span = meta_div.find('span', class_='descriptor')
			if title_span and title_span.next_sibling: 
				paper.title = title_span.next_sibling.strip(' "')

			authors_div = meta_div.find('div', class_='list-authors')
			if authors_div: 
				authors = [a.get_text(strip=True) for a in authors_div.find_all('a')]
				paper.authors = authors

			subject_span = meta_div.find('span', class_='primary-subject')
			if subject_span: 
				paper.subjects.append(subject_span.get_text(strip=True))
				extra_subjects = subject_span.next_sibling.strip(' "')
				extra_subjects.rstrip('\n')
				paper.subjects.append(extra_subjects)

		article_list.append(paper)

		if iter == max_papers: 
			break

		iter += 1

	return article_list

if __name__ == "__main__": 
	topics = create_topis_dict()

	parser = argparse.ArgumentParser()
	parser.add_argument("--topic", "-t", type=str, help="Choose topic. use hyphens instead of spaces", required=True)
	parser.add_argument("--abstract", "-a", type=bool, help="Display the abstract. Default = True", default=True, required=False)
	parser.add_argument("--num", "-n", type=int, help="Choose how many papers to display", default=25, required=False)

	args = parser.parse_args()

	if args.topic in topics:
		topic_url = topics[args.topic]
		getInfo(topic_url, args.abstract, args.num)
	else: 
		print(f"-The topic: {args.topic} is not a valid topic.")
		print("-You may have a typo or the topic does not contain a valid list of papers.")
		print("-Head to https://arxiv.org to view the list of topics available on the arxiv website.")
