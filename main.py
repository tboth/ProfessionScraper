#!/usr/bin/python3

import subprocess
import json
import lxml
import time
from bs4 import BeautifulSoup

URL = "https://www.profession.hu/allasok/1,0,0,Data%2Bscientist%25401%25401?keywordsearch/"

website_call = subprocess.run(["curl", URL], stdout=subprocess.PIPE)

s = BeautifulSoup(website_call.stdout, "lxml")
links = [element.a['href'] for element in  s.find_all('h2', class_= '''job-card__title text-truncate''')]

results = []

for link in links:
	website_call = subprocess.run(["curl", link], stdout=subprocess.PIPE)
	soup = BeautifulSoup(website_call.stdout, "lxml")
	header = soup.find("header", class_ = "adv-cover-header")
	results.append( 
	{
	"title" : header.h1.text,
	"company" : header.h2.text,
	"place_of_work" : header.h3.text,
	"description" : soup.select('[id*="sablon"]')
	})

for result in results:
	print(result)
