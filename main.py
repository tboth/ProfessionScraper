#! /usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
import csv
import argparse
from datetime import date

# argument parsing - segiteni fog hogy 1 topicban(hely, nyelvtudas, szakma, stb.) csak 1 scriptet kelljen hasznalni
# dinamikusan valtozik 3 adat:
# 1. file neve -> -f vagy --filename opcioval, eleg csak megadni a kategoriat, pl. 'adm-ass-office'
# 2. URL valtozo resze -> -u vagy --url_part opcioval, altalaban szoveggel van megadva 1 resz, ezt ide kell beirni, pl. 'adminsztracio-asszisztens-irodai-munka'
# 3. kategoria -> -c vagy --category, kimeneti file-ben megjelolt kategoria, pl. 'administration-assistance-office-work'' 
parser = argparse.ArgumentParser()
parser.add_argument('-f', '--filename', help='Filename', required=True)
parser.add_argument('-u', '--url_part', help='URL changing part', required=True)
parser.add_argument('-c', '--category', help='Category name', required=True)
args = vars(parser.parse_args())

#eleg egyszer lekerni a mai datumot
today_column = str(date.today())

csv_file = open(today_column  + "_" + args['filename'] + ".csv", "w")

csv_writer = csv.writer(csv_file, delimiter=';')
csv_writer.writerow(['Job Name', 'Company', 'Place', 'Highlights', 'Category', 'Date'])

job_category = args['category']
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

#darabaszam kiszedese az oldalbol
#ugy oldottam meg hogy lesz +1 request az elso oldalra
#megtalahato hogy osszesen hany darab hirdetes van az adott kategoriaban
#ezt osztom az oldalankenti darabszammal es megvagyunk

#===> atirni az elso oldal URL-jet
url = "https://www.profession.hu/allasok/{}/1,1".format(args['url_part'])
html_page = requests.get(url, headers=headers)
soup = BeautifulSoup(html_page.content, 'lxml')
total_jobs_div = soup.find("div", class_ = "job-list__count head d-flex align-items-center justify-content-between")
total_jobs_in_category = int(total_jobs_div.get_text().strip().replace("\n","").split(" ")[0])

num_of_pages = (total_jobs_in_category // 20) + 1
if total_jobs_in_category % 20 > 0: num_of_pages += 1

#------------------------------------------------------------------------------------------
#kommentek az eredeti kodhoz:
# a ciklusvaltozot lehet hasznalni a ciklusban
# url_count, count, highlight_count - eleg helyettuk a ciklusvaltozo

# try - except: break -> hatalmas antipattern
# legalabb azt meg kell jelolni hogy milyen errort varunk (ValueError, AttributeError, stb.)
#------------------------------------------------------------------------------------------
time.sleep(5)
for i in range(1,num_of_pages):
#===> megfigyelni hogy hogyan valtozik az URL es az szerint beallitani a valtozo adatokat (kategoria, oldalszam)
    url = "https://www.profession.hu/allasok/{}/{},1".format(args['url_part'],i)
    html_page = requests.get(url, headers=headers)
    soup = BeautifulSoup(html_page.content, 'lxml')
    job_cards = soup.find_all("div", class_ = "card-body")
    
    #for ciklus for/eachre valtoztatva
    for job_card in job_cards:
        if job_card:
            
            # job[] tombot lehet egyszerubben is hozzaadni a vegen, igy megsporolunk nehany sort

            #nehany dolog valtozott miota meg lett irva a scraper(HTML elnevezesek, struktura)
            job_name = job_card.find_all("a")[0].get_text().strip().replace("\n","")
            company = job_card.find("a", class_ = "link-icon").get_text().strip().replace("\n","")
            place = job_card.find("div", class_ = "job-card__company-address newarea mt-2 mt-md-0 icon map").get_text().strip().replace("\n","")
            
            #higlights block at lett irva 
            #2 kulonbozo div van, mindkettoben megkeresem a cimszavakat es egyesitem egy tombbe

            #list comprehension-t hasznaltam (lenyegeben ugyanaz mint a for/each ciklus csak rovidebb)
            highlights = [element.get_text().strip().replace("\n","") for element in job_card.find_all("span", class_="advertisement_tag job-card__tag job-card__tag--stress-call")]
            highlights.extend([element.get_text().strip().replace("\n","") for element in job_card.find_all("span", class_="advertisement_tag job-card__tag")])
            job_highlights = "Highlights: " + " &".join(highlights)
            csv_writer.writerow([job_name, company, place, job_highlights, job_category, today_column])
    time.sleep(5)

csv_file.close()
