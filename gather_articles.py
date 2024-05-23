from __future__ import annotations
from dataclasses import dataclass, field
from typing import List
from bs4 import BeautifulSoup
import requests
import webbrowser
import pathlib


@dataclass
class Paper(): 
	title: str
	authors: List[str]
	pdf_link: str
	date: str
	subjects: List[str]
	abstract: str = field(default="")
	keywords: List[str] = field(default_factory=list)

	def display(self):
		if len(self.abstract) != 0:
			return (
				f"Title: {self.title}\n"
				f"Author: {self.author}\n"
				f"Publication Year: {self.publication_year}\n"
				f"PDF Link: {self.pdf_link}\n"
				f"Abstract: {self.abstract}\n"
				f"Keywords: {', '.join(self.keywords)}")
		else: 
			return (
				f"Title: {self.title}\n"
				f"Author: {self.author}\n"
				f"Publication Year: {self.publication_year}\n"
				f"PDF Link: {self.pdf_link}\n")

	def open_pdf(self): 
		# TODO add safety checks here
		webbrowser.open(self.pdf_link)


def getInfo():
	# TODO: add support for other links
	url: str = "https://arxiv.org/list/cs.AI/recent"
	response = requests.get(url)
	html_content = response.content

	soup = BeautifulSoup(html_content, 'html.parser')
	print(soup.prettify())

	if soup: 
		dl_tag = soup.find('id', id='dlpage')
		if dl_tag: 
			parse_articles(dl_tag)
			print(dl_tag.prettify())
		else: 
			print("Error: Could not find dl tag with articles.")


def parse_articles(dl_tag): 
	# links for each article inside the <dt> header
	# the meta information like title and authors is inside the <dd> <div class="meta"> tag
	pass


if __name__ == "__main__": 
	# TODO add parsing information to display certain parts and load articles in web page potentially