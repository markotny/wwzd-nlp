import requests
from bs4 import BeautifulSoup
import os
import shutil
from pymaybe import maybe
import time
import multiprocessing
from joblib import Parallel, delayed
from tqdm import tqdm

# detect the current working directory and print it
working_dir = os.getcwd()

parties_dir = working_dir + '\\partie'

try:
    os.mkdir(parties_dir)
except OSError:
    shutil.rmtree(parties_dir)
    os.mkdir(parties_dir)

base_url = 'https://www.sejm.gov.pl/Sejm9.nsf'

workers_url = base_url + '/agent.xsp?symbol=RWYSTAPIENIA&NrKadencji=9'
res = requests.get(workers_url)
html_page = res.content
soup = BeautifulSoup(html_page, 'html.parser')

speakers = []
parties = []

table_body = soup.find("table", {"class":"tab"})
rows = table_body.find('tbody')

def listToString(text_list):  
    return_string = ""  
    
    for element in text_list:  
        return_string += element + "\n"
    return return_string

def prepare_pagination(link):
    links = []
    res = requests.get(base_url + "/" + link)
    html = res.content
    speaker_soup = BeautifulSoup(html, 'html.parser')
    nav = speaker_soup.find('ul', {'class': 'pagination'})
    lists = maybe(nav).find_all('li')
    if lists:
        lists = lists[1:-1]
        lists_count = len(lists)
        for i in range(1, lists_count):
            links.append(link + '&page=' + str(i))
        return links
    links.append(link)
    return links

def prepare_rows(link):
    res = requests.get(base_url + "/" + link)
    html = res.content
    speaker_soup = BeautifulSoup(html, 'html.parser')
    return speaker_soup.find('tbody')

def prepare_text(link):
    res = requests.get(base_url + '/' + link)
    html = res.content
    text_soup = BeautifulSoup(html, 'html.parser')
    stenogram = text_soup.find("div", {"class": "stenogram"})
    try:
        maybe(stenogram.find('h2', {"class": "punkt"})).decompose()
        maybe(stenogram.find('p', {"class": "punkt-tytul"})).decompose()
        maybe(stenogram.find('h2', {"class": "mowca"})).decompose()
    except Exception as e:
        print(e)
        print(link)
    html_text = stenogram.find_all('p')
    text_list = [x.getText() for x in html_text]
    return listToString(text_list)

def process_speaker(speaker):
    speaker_party = speaker['party']
    speaker_name = speaker['name']
    speaker_link = speaker['link']
    speaker_dir = parties_dir + '\\' + speaker_party + '\\' + speaker_name
    os.mkdir(speaker_dir)
    links = prepare_pagination(speaker_link)
    for link in links:
        rows = prepare_rows(link)
        for row in rows:
            row_content = row.find_all('td')
            link = row_content[4].find('a', href=True)['href']
            date = row_content[2].getText()
            text = prepare_text(link)
            with open(speaker_dir + '\\' + date + '.txt', 'a') as f:
                f.write(text)

for row in rows:
    row_content = row.find_all('td')
    speaker = {
        "name": row_content[1].getText(),
        "link": row_content[3].find('a', href=True)['href'],
        "party": row_content[2].getText()
    }
    
    parties.append(row_content[2].getText())
    speakers.append(speaker)

# reduce duplicates
parties = list(dict.fromkeys(parties))

# create party folders
for party in parties:
    os.mkdir(parties_dir + '\\' + party)

# speaker = speakers[183]
# process_speaker(speaker)
# for speaker in speakers:
#     process_speaker(speaker)

num_cores = multiprocessing.cpu_count()
inputs = tqdm(speakers)

Parallel(n_jobs=num_cores)(delayed(process_speaker)(i) for i in inputs)