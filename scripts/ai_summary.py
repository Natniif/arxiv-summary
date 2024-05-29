import pymupdf
import requests
import torch 
import transformers

def get_pdf_text(url: str) -> str:
	response = requests.get(url)
	pdf_data = response.content

	doc = pymupdf.open(stream=pdf_data, filetype='pdf')
	text = ""
	for page in doc: 
		text += page.get_text()

	return text

if __name__ == '__main__': 
	print(get_pdf_text('https://arxiv.org/pdf/2405.18377'))

