import requests as req
import os
from bs4 import BeautifulSoup as bs
import sys

# Paper ID in arxiv
pid = sys.argv[1]

# Construct url
url_abs = "https://arxiv.org/abs/" + pid 
url_pdf = "https://arxiv.org/pdf/" + pid 

web_abs = req.request("get", url_abs)
web_pdf = req.request("get", url_pdf)

soup = bs(web_abs.text, features="html.parser")
title = soup.title.string[13:]
authors = [link.get("content") for link in soup.find_all("meta", attrs={"name": "citation_author"})]
abstract = soup.find("blockquote").text[12:-6]

if os.path.isdir(pid):
  pass
else:
  os.mkdir(pid)

with open(f"{pid}/{pid}.pdf", 'wb') as f:
  f.write(web_pdf.content)

with open(f"{pid}/{pid}.enw", 'w') as f:
  f.write("%0 Electronic Article\n")
  f.write(f"%T {title}\n")
  for author in authors:
    f.write(f"%A {author}\n")
  f.write(f"%U {url_abs}\n")
  f.write(f"%X {abstract}\n")
  f.write(f"%> {os.getcwd()}/{pid}/{pid}.pdf")
