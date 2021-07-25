#! /usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import csv
from datetime import date

#file nevet nem muszaj valtozoba tenni
today_column = str(date.today())
csv_file = open(today_column  + "_adm_ass_office.csv", "w")

csv_writer = csv.writer(csv_file, delimiter=';')
csv_writer.writerow(['Job Name', 'Company', 'Place', 'Highlights', 'Category', 'Date'])

job_category = "administration-assistance-office-work"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

# a ciklusvaltozot lehet hasznalni a ciklusban
# url_count, count, highlight_count - eleg helyettuk a ciklusvaltozo

# try - except: break -> hatalmas antipattern
# legalabb azt meg kell jelolni hogy milyen errort varunk (ValueError, AttributeError, stb.)
# plusz valami 
for url_count in range(5):
    url = "https://www.profession.hu/allasok/adminisztracio-asszisztens-irodai-munka/{},1".format(url_count)
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'lxml')
    job_cards = soup.find_all("div", class_ = "card-body")
    
    #for ciklus for-eachre valtoztatva
    for job_card in job_cards:
        if job_card:
            
            # ez a job tomb felesleges volt, nem kell minden ciklusban letrehozni, mivel az egyetlen funkcioja az hogy
            # a fajlba irasnal beleirjuk a tombot
            # job = []

            #nehany dolog valtozott miota meg lett irva a scraper(HTML elnevezesek, struktura)
            job_name = job_card.find_all("a")[0].get_text().strip().replace("\n","")
            company = job_card.find("a", class_ = "link-icon").get_text().strip().replace("\n","")
            place = job_card.find("div", class_ = "job-card__company-address newarea mt-2 mt-md-0 icon map").get_text().strip().replace("\n","")
            
            #higlights block at lett irva 
            #2 kulonbozo div van, mindkettoben megeresem a cimszavakat es egyesitem egy tombbe

            #list comprehension-t hasznaltam (lenyegeben ugyanaz mint a for/each ciklus csak rovidebb)
            highlights = [element.get_text().strip().replace("\n","") for element in job_card.find_all("span", class_="advertisement_tag job-card__tag job-card__tag--stress-call")]
            highlights.extend([element.get_text().strip().replace("\n","") for element in job_card.find_all("span", class_="advertisement_tag job-card__tag")])
            job_highlights = "Highlights: " + " &".join(highlights)
            print([job_name, company, place, job_highlights, job_category, today_column])
            csv_writer.writerow([job_name, company, place, job_highlights, job_category, today_column])
    time.sleep(5)

csv_file.close()
