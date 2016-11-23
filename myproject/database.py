from bills.models import Introducer, Bill
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def getIntroducers():
    
    r= requests.get("http://nebraskalegislature.gov/bills/")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    lists = soup.find_all('select')
    
    introducers = lists[4].find_all('option')
    introducers.pop(0)
    introducers_list = []
    for introducer in introducers:
        introducer_text = introducer.text.split(',')
        if len(introducer_text) == 3:
            introducer_name = introducer_text[0] + "," + introducer_text[2]
        elif len(introducer_text) < 3:
            introducer_name = introducer_text[0]
        else:
            introducer_name = introducer_text[0]
            print("ERROR getting introducer name:", introducer_name)
        introducer_value = introducer['value']
        introducers_list.append((introducer_value, introducer_name))
        print(introducer_value, introducer_name)
    return introducers_list

def updateIntroducers(introducers):
    for introducer in introducers:
        obj, created = Introducer.objects.update_or_create(introducer_id=str(introducer[0]), introducer_name = introducer[1], defaults = {'introducer_id' : str(introducer[0]), 'introducer_name' : introducer[1]})
        print(obj, created)
        
def updateBills(introducers):
    for introducer in introducers:
        r = requests.get("http://nebraskalegislature.gov/bills/search_by_introducer.php?Introducer=%s&CoSponsor=Y" % str(introducer[0]))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        bills = soup.find('tbody').find_all('tr')
        if len(bills) > 0:
            for bill in bills:
                bill_number = bill.find_all('a')[0].text
                bill_name = bill.find_all('td')[3].text.strip()
                bill_link = bill.find_all('a')[0]['href']
                bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
                introducer_name = bill.find_all('a')[1].text
                introducer_link = bill.find_all('a')[1]['href'].split('&')[0]
                introducer_id = re.match('.*?([0-9]+)$', introducer_link).group(1)
                status = bill.find_all('td')[2].text.strip()
                r = requests.get("http://nebraskalegislature.gov/bills/view_bill.php?DocumentID=%s" % str(bill_id))
                data = r.text
                soup = BeautifulSoup(data, 'html.parser')
                bill_info = soup.find_all('ul', class_='list-unstyled')
                document_info = bill_info[0].find_all('li')
                introduction_date = document_info[1]
                introduction_date_text = introduction_date.text.split(":")[1].strip()
                introduction_date_link = introduction_date.find('a')['href']
                introduction_date_date = re.match('.*?([0-9-]+)$', introduction_date_link).group(1)
                text_copies = bill_info[1].find_all('li')
                text_copies_list = []
                for text_copy in text_copies:
                    text_copy_text = text_copy.text
                    text_copy_link = text_copy.find('a')['href']
                    text_copies_list.append((text_copy_text, text_copy_link))
                additional_info_list = []
                if len(bill_info) == 3:
                    additional_info = bill_info[2].find_all('li')
                    for additional in additional_info:
                        additional_text = additional.text
                        additional_link = additional.find('a')['href']
                        additional_info_list.append((additional_text, additional_link))
                history = soup.find_all('div', class_="col-sm-8")[1].find('tbody').find_all('tr')
                history_list = []
                for history_item in history:
                    history_item_info = history_item.find_all('td')
                    history_item_date_text = history_item_info[0].text
                    history_item_date = datetime.strptime(history_item_date_text, '%b %d, %Y')
                    history_item_action = history_item_info[1].text
                    history_item_link = history_item_info[2].find('a')['href']
                    history_item_link_text = history_item_info[2].find('a').text
                    history_list.append((history_item_date, history_item_action, history_item_link_text, history_item_link))
                proposed_amendments = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[1].find_all('tr')
                proposed_amendments_list = []
                for proposed_amendment in proposed_amendments:
                        proposed_amendment_text = proposed_amendment.text.strip().split('\n\n\n')
                        proposed_amendment_proposer = proposed_amendment_text[0]
                        proposed_amendment_status = proposed_amendment_text[1].strip()
                        proposed_amendment_link = proposed_amendment.find('a')['href']
                        proposed_amendments_list.append((proposed_amendment_proposer, proposed_amendment_status, proposed_amendment_link))
                related_transcripts = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[2].find_all('td')
                related_transcripts_list = []
                for related_transcript in related_transcripts:
                    related_transcript_text = related_transcript.text
                    related_transcript_link = related_transcript.find('a')['href']
                    related_transcripts_list.append((related_transcript_text, related_transcript_link))
                
                i = Introducer.objects.get(introducer_id = introducer[0])
                b, created = Bill.objects.get_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'introduction_date':introduction_date_date, 'status':status})
                for history in history_list:
                    b.history_set.update_or_create(date = history[0], defaults={'date':history[0], 'action':history[1], 'journal_page':history[2]})
                for amendment in proposed_amendments_list:
                    b.amendment_set.update_or_create(proposer = amendment[0], defaults = {'proposer':amendment[0], 'link':amendment[2]})
                for transcript in related_transcripts_list:
                    b.transcript_set.update_or_create(name = transcript[0], defaults={'name':transcript[0], 'link':transcript[1]})
                for text in text_copies_list:
                    b.textcopy_set.update_or_create(name = text[0], defaults={'name':text[0], 'link':text[1]})
                for info in additional_info_list:
                    b.additionalinfo_set.update_or_create(name = info[0], defaults={'name':info[0], 'link':info[1]})
                b.introducer_id.add(i)
                
                
                
                print(introducer_name, bill_number, created)
        else: 
            print("No bills for", introducer_name)
        
        
def getDays():
    r= requests.get("http://nebraskalegislature.gov/bills/")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    lists = soup.find_all('select')
    days = lists[3].find_all('option')
    days.pop(0)
    days_list = []
    for day in days:
        day_name = day.text
        day_value = day['value']
        days_list.append((day_value, day_name))
        print(day_name)
        
    return days_list

def getBillsbyDay(days):
    for day in days:
        r = requests.get("http://nebraskalegislature.gov/bills/search_by_date.php?SessionDay=%s" % str(day[0]))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        bills = soup.find('tbody').find_all('tr')
        bills_list = []
        if len(bills) > 0:
            for bill in bills:
                bill_number = bill.find_all('a')[0].text
                bill_name = bill.find_all('td')[3].text.strip()
                bill_link = bill.find_all('a')[0]['href']
                bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
                introducer_name = bill.find_all('a')[1].text
                introducer_link = bill.find_all('a')[1]['href'].split('&')[0]
                introducer_id = re.match('.*?([0-9]+)$', introducer_link).group(1)
                status = bill.find_all('td')[2].text.strip()
                bills_list.append((bill_id, bill_number, bill_name, bill_link, introducer_name, introducer_id, status))
                print(bill_number)
        else: 
            print("No bills for", day_name)
        
    return bills_list


    