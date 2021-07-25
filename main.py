#!/usr/bin/python3

import subprocess
import json
import lxml
import time
from bs4 import BeautifulSoup

results = []

#ezt ki kell javitani - kulso for ciklus
for i in range(1,5):
	URL = f"https://www.profession.hu/allasok/{i},0,0,Data+scientist%25401%25401?keywordsearch"
	website_call = subprocess.run(["curl", URL], stdout=subprocess.PIPE)

	s = BeautifulSoup(website_call.stdout, "lxml")
	links = [element.a['href'] for element in  s.find_all('h2', class_= '''job-card__title text-truncate''')]

	for link in links:
		try:
			website_call = subprocess.run(["curl", link], stdout=subprocess.PIPE)
			soup = BeautifulSoup(website_call.stdout, "lxml")
			header = soup.find("header", class_ = "adv-cover-header")
			description = soup.select('[id*="sablon"]')
			description_text = "\n".join([element.strip() for element in description[0].findAll(text=True) if element != '\n'])
			results.append( 
			{
				"title" : header.h1.text,
				"company" : header.h2.text,
				"place_of_work" : header.h3.text,
				"description" : description_text
			})
		except:
			AttributeError
			continue
		time.sleep(1)

with open(time.strftime("%Y-%m-%d_%H:%M:%S") + '.json', 'w', encoding='utf-8') as f:
	json.dump(results, f)