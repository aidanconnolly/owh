#This script gets all of the bills presented on a specific day. Information includes the bill name (LB ###), the link to the bill, the DocumentID (used in billScraper.py), the introducer name, the link to the introducer, the IntroducerID (used in introducerScraper.py), the status and a description. These are all saved in bills_list.

import requests
import re
from bs4 import BeautifulSoup

def dayScraper(day):
    print('Getting html structure...')
    r= requests.get("http://nebraskalegislature.gov/bills/search_by_date.php?SessionDay=%s" % day)
    data = r.text
    
    print('Parsing html structure...')
    soup = BeautifulSoup(data, "html.parser")
    
    bills = soup.find('tbody').find_all('tr')
    bills_list = []
    
    print('\tGetting bills...')
    for bill in bills:
        bill_name = bill.find_all('a')[0].text
        bill_link = bill.find_all('a')[0]['href']
        bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
        introducer_name = bill.find_all('a')[1].text
        introducer_link = bill.find_all('a')[1]['href'].split('&')[0]
        introducer_id = re.match('.*?([0-9]+)$', introducer_link).group(1)
        status = bill.find_all('td')[2].text.strip()
        description = bill.find_all('td')[3].text.strip() 
        bills_list.append((bill_name, bill_link, bill_id, introducer_name, introducer_link, introducer_id, status, description))
        print(bill_name)
        
    
    print("\n", len(bills_list), "bills collected.")
        
dayScraper("2016-01-06")