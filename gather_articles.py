from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Union
from bs4 import BeautifulSoup
import requests
import webbrowser
import pathlib

BASE_URL = "https://arxiv.org/"

@dataclass
class Paper:
	title: str = ""
	authors: List[str] = field(default_factory=list)
	pdf_link: str = ""
	subjects: List[str] = field(default_factory=list)
	abstract: str = ""

	def __repr__(self):
		if len(self.abstract) != 0:
			return (
				f"\n"
				f"Title: {self.title}\n"
				f"Authors: {self.authors}\n"
				f"Publication Year: {self.date}\n"
				f"PDF Link: {self.pdf_link}\n"
				f"Abstract: {self.abstract}\n"
				f"subjects: {', '.join(self.subjects)}"
				f"\n")
		else: 
			return (
				f"\n"
				f"Title: {self.title}\n"
				f"Authors: {self.authors}\n"
				f"PDF Link: {self.pdf_link}\n"
				f"subjects: {', '.join(self.subjects)}"
				f"\n")

	def open_pdf(self): 
		# TODO add safety checks here
		webbrowser.open(self.pdf_link)


def getInfo():
	# TODO: add support for other links
	url: str = "https://arxiv.org/list/cs.AI/recent"
	response = requests.get(url)
	html_content = response.content

	soup = BeautifulSoup(html_content, 'html.parser')

	if soup: 
		dl_tag = soup.find('dl', id='articles')
		if dl_tag: 
			article_list = parse_articles(dl_tag)
		else: 
			print("Error: Could not find dl tag with articles.")

	print(article_list)

def extract_abstract(abstract_link)-> Union[str, None]: 
	url: str = abstract_link
	response = requests.get(url)
	html_content = response.content
	soup = BeautifulSoup(html_content, 'html.parser')

	abstract_div = soup.find('blockquote', class_='abstract mathjax')
	if abstract_div: 
		abstract_text = abstract_div.get_text(strip=True)
	else: 
		return None

	return abstract_text

def parse_articles(dl_tag): 
	# links for each article inside the <dt> header
	# the meta information like title and authors is inside the <dd> <div class="meta"> tag

	article_list = []

	dt_tags = dl_tag.find_all('dt')
	dd_tags = dl_tag.find_all('dd')

	for dt, dd in zip(dt_tags, dd_tags):
		# links 
		paper = Paper()
		pdf_link = dt.find('a', title="Download PDF")['href'] if dt.find('a', title='Download PDF') else ''
		paper.pdf_link = BASE_URL + pdf_link 

		# abstract_link = BASE_URL + dt.find('a', title='Abstract')['href']
		# if abstract_link: 
		# 	paper.abstract = extract_abstract(abstract_link)

		meta_div = dd.find('div', class_='meta')
		if meta_div: 

			title_span = meta_div.find('span', class_='descriptor')
			if title_span and title_span.next_sibling: 
				paper.title = title_span.next_sibling.strip(' "')

			authors_div = meta_div.find('div', class_='list-authors')
			if authors_div: 
				authors = [a.get_text(strip=True) for a in authors_div.find_all('a')]
				paper.authors = authors

			subject_span = meta_div.find('span', class_='primary_subject')
			if subject_span and subject_span.next_sibling: 
				paper.title = title_span.next_sibling.strip(' "')

		article_list.append(paper)

	return article_list

if __name__ == "__main__": 
	# TODO add parsing information to display certain parts and load articles in web page potentially

	getInfo()
	pass