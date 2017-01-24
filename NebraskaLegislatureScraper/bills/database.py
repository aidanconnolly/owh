from models import Senator, Committee, Bill, History, ConsideredAmendment, ProposedAmendment, Transcript, TextCopy, AdditionalInfo
import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

def getSenators():

    # This function gets the list of senators from the nebraskalegislature.gov/bills dropdown list. The list is returned with the senator id, which is used for searches, and the senator name.
    # This function does not get a complete list of senators. There are some bills on the website that were introduced by a senator not in the list. Unlesss those senators are manually added, those bills cannot be added and the bill script breaks.
    
    r= requests.get("http://nebraskalegislature.gov/bills/")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    lists = soup.find_all('select')
    
    senators = lists[4].find_all('option')
    # This removed the "Select a senator" option
    senators.pop(0)
    senators_list = []
    for senator in senators:

        # This gets the name of the senator from the list, which includes the name and the district number. 
        senator_text = senator.text.split(',')
        # This case is for the executive board chairperson
        if len(senator_text) == 3:
            senator_name = senator_text[0] + "," + senator_text[2]
        # This case is for the other senators
        elif len(senator_text) < 3:
            senator_name = senator_text[0]
        # This catches anything weird that might be added
        else:
            senator_name = senator_text[0]
            print("ERROR getting senator name:", senator_name)
        senator_value = senator['value']
        senators_list.append((senator_value, senator_name))
        print(senator_value, senator_name)
    return senators_list

def getCommittees():

    # This function gets the list of committees from the nebraskalegislature.gov/bills dropdown list. The issue is that some committees do not have the full name listed. Some are missing the word committee. So, if the name does not end in committee, it is added. This is not the best practice but it works. For now.
    committees_list = []
    r=requests.get("http://nebraskalegislature.gov/bills/")
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    lists = soup.find_all('select')
    committees = lists[5].find_all('option')
    # This removes the "Select a committee" option
    committees.pop(0)
    for committee in committees:
        committee_name = committee.text
        committee_value = committee['value']
        # Here, regex finds the last word of the name.
        last_word = re.match('.*?(\(*[A-Za-z0-9]+\)*)$', committee_name).group(1)
        # If the last word is not committee, it is added to try and match the full name
        if last_word != "Committee":
            committee_name = committee_name + " Committee"
        committees_list.append((committee_value, committee_name))
        print(committee_value, committee_name)
    return committees_list

def updateSenators(senators):
    # This function takes the list of senators and makes sure they are all in the database. If not, they're added. 
    for senator in senators:
        obj, created = Senator.objects.update_or_create(id=str(senator[0]), name = senator[1], defaults = {'id' : str(senator[0]), 'name' : senator[1]})
        print(obj, created)
   
def updateCommittees(committees):
    # This function takes the list of committees and makes sure they are all in the database. If not, they're added.
    for committee in committees:
        obj, created = Committee.objects.update_or_create(id=str(committee[0]), defaults = {'id':str(committee[0]), 'name':committee[1]})
        print(obj, created)
     
def updateSenatorBills():
    # This function goes through the database of senators and adds each senator's bills to the database.
    # If a bill is found on a senator's search page, it is updated or created with the senator listed as a co-sponsor, unless the senator is the primary introducer.
    # Keep in mind, if a bill is found that was introduced by a senator not in the database, the script will break.
    # Also, there is a function below that does the same thing for committees. If you make any changes to this function, please make the same changes in that function.
    senators = Senator.objects.all()
    for introducer in senators:
        r = requests.get("http://nebraskalegislature.gov/bills/search_by_introducer.php?Introducer=%s&CoSponsor=Y" % str(introducer.id))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('tbody')
        if table != None:
            bills = table.find_all('tr')
            for bill in bills:
                bill_number = bill.find_all('a')[0].text
                bill_name = bill.find_all('td')[3].text.strip()
                bill_link = bill.find_all('a')[0]['href']
                bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
                primary_introducer_name = bill.find_all('a')[1].text
                primary_introducer_link = bill.find_all('a')[1]['href'].split('&')[0]
                primary_introducer_id = re.match('.*?([0-9]+)$', primary_introducer_link).group(1)
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
                considered_amendments = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[0].find_all('tr')
                considered_amendments_list = []
                for considered_amendment in considered_amendments:
                        considered_amendment_text = considered_amendment.text.strip().split('\n\n\n')
                        considered_amendment_name = considered_amendment_text[0]
                        considered_amendment_status = considered_amendment_text[1].strip()
                        considered_amendment_link = considered_amendment.find('a')['href']
                        considered_amendments_list.append((considered_amendment_name, considered_amendment_status, considered_amendment_link))
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

                # This resets the variables for adding the primary introducer and co-sponsors
                primary_senator = None
                primary_committee = None
                co_sponsor = None

                # Because the primary introducer can be a senator or a committee, both have to be searched for the primary_introducer_id and primary_introducer_name
                try:
                    primary_senator = Senator.objects.get(id = primary_introducer_id, name = primary_introducer_name)
                except:
                    pass

                try:
					primary_committee = Committee.objects.get(id = primary_introducer_id, name = primary_introducer_name)
                except:
                    pass

                # I believe only senators can be co-sponsors, so this tries to get the senator object for that purpose.
                try:
					co_sponsor = Senator.objects.get(id = introducer.id, name = introducer.name)
                except:
                    pass
                            
                # Here, the bill is updated or created with the information. It adds either a senator_primary_sponsor or a committee_primary_sponsor based on which variable is not null. If somehow both are null, something went wrong.
                if primary_senator != None:
					b, created = Bill.objects.update_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'senator_primary_sponsor':primary_senator, 'introduction_date':introduction_date_date, 'status':status})	
                elif primary_committee != None:
					b, created = Bill.objects.update_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'committee_primary_sponsor': primary_committee, 'introduction_date':introduction_date_date, 'status':status})	
                else:
					b, created = Bill.objects.update_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'introduction_date':introduction_date_date, 'status':status})
					print("BILL CREATED WITHOUT PRIMARY INTRODUCER")

                #Here, all of the corresponding information and documents are saved to the database
                for history in history_list:
                    b.history_set.update_or_create(date = history[0], defaults={'date':history[0], 'action':history[1], 'journal_page':history[2]})
                for amendment in proposed_amendments_list:
                    b.consideredamendment_set.update_or_create(name = amendment[0], defaults = {'name':amendment[0], 'status':amendment[1], 'link':amendment[2]})
                for amendment in proposed_amendments_list:
                    b.proposedamendment_set.update_or_create(proposer = amendment[0], defaults = {'proposer':amendment[0], 'status':amendment[1], 'link':amendment[2]})
                for transcript in related_transcripts_list:
                    b.transcript_set.update_or_create(name = transcript[0], defaults={'name':transcript[0], 'link':transcript[1]})
                for text in text_copies_list:
                    b.textcopy_set.update_or_create(name = text[0], defaults={'name':text[0], 'link':text[1]})
                for info in additional_info_list:
                    b.additionalinfo_set.update_or_create(name = info[0], defaults={'name':info[0], 'link':info[1]})
                
                #Finally, if the co-sponsor variable is not null and the co-sponsor is not the primary_senator or already a co-sponsor, the co-sponsor is added.
                if co_sponsor != None and co_sponsor != primary_senator and co_sponsor != primary_committee and co_sponsor not in b.co_sponsors.all():
					b.co_sponsors.add(co_sponsor)
                
                
                
                print(introducer.name, bill_number, created)
        else: 
            print("No bills for", introducer.name)
        

def updateCommitteeBills():
    # This function goes through the database of committees and adds each committee's bills to the database.
    # If a bill is found on a committee's search page, it is updated or created with the committee listed as a co-sponsor, unless the committee is the primary introducer.
    # Keep in mind, if a bill is found that was introduced by a committee not in the database, the script will break.
    # Also, there is a function above that does the same thing for senators. If you make any changes to this function, please make the same changes in that function.
    committees = Committee.objects.all()
    for introducer in committees:
        r = requests.get("http://nebraskalegislature.gov/bills/search_by_introducer.php?Introducer=%s&CoSponsor=Y" % str(introducer.id))
        data = r.text
        soup = BeautifulSoup(data, "html.parser")
        table = soup.find('tbody')
        if table != None:
            bills = table.find_all('tr')
            for bill in bills:
                bill_number = bill.find_all('a')[0].text
                bill_name = bill.find_all('td')[3].text.strip()
                bill_link = bill.find_all('a')[0]['href']
                bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
                primary_introducer_name = bill.find_all('a')[1].text
                primary_introducer_link = bill.find_all('a')[1]['href'].split('&')[0]
                primary_introducer_id = re.match('.*?([0-9]+)$', primary_introducer_link).group(1)
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
                considered_amendments = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[0].find_all('tr')
                considered_amendments_list = []
                for considered_amendment in considered_amendments:
                        considered_amendment_text = considered_amendment.text.strip().split('\n\n\n')
                        considered_amendment_name = considered_amendment_text[0]
                        considered_amendment_status = considered_amendment_text[1].strip()
                        considered_amendment_link = considered_amendment.find('a')['href']
                        considered_amendments_list.append((considered_amendment_name, considered_amendment_status, considered_amendment_link))
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

                # This resets the variables for adding the primary introducer and co-sponsors
                primary_senator = None
                primary_committee = None
                co_sponsor = None

                # Because the primary introducer can be a senator or a committee, both have to be searched for the primary_introducer_id and primary_introducer_name
                try:
                    primary_senator = Senator.objects.get(id = primary_introducer_id, name = primary_introducer_name)
                except:
                    pass

                try:
					primary_committee = Committee.objects.get(id = primary_introducer_id, name = primary_introducer_name)
                except:
                    pass

                # I believe only senators can be co-sponsors, so this shouldn't ever do anything.
                try:
					co_sponsor = Committee.objects.get(id = introducer.id, name = introducer.name)
                except:
                    pass
             
                # Here, the bill is updated or created with the information. It adds either a senator_primary_sponsor or a committee_primary_sponsor based on which variable is not null. If somehow both are null, something went wrong.
                if primary_senator != None:
					b, created = Bill.objects.get_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'senator_primary_sponsor':primary_senator, 'introduction_date':introduction_date_date, 'status':status})	
                elif primary_committee != None:
					b, created = Bill.objects.get_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'committee_primary_sponsor': primary_committee, 'introduction_date':introduction_date_date, 'status':status})	
                else:
					b, created = Bill.objects.get_or_create(bill_id=bill_id, defaults={'bill_id':bill_id, 'bill_number':bill_number, 'bill_name':bill_name, 'introduction_date':introduction_date_date, 'status':status})
					print("BILL CREATED WITHOUT PRIMARY INTRODUCER")

                #Here, all of the corresponding information and documents are saved to the database
                for history in history_list:
                    b.history_set.update_or_create(date = history[0], defaults={'date':history[0], 'action':history[1], 'journal_page':history[2]})
                for amendment in proposed_amendments_list:
                    b.consideredamendment_set.update_or_create(name = amendment[0], defaults = {'name':amendment[0], 'status':amendment[1], 'link':amendment[2]})
                for amendment in proposed_amendments_list:
                    b.proposedamendment_set.update_or_create(proposer = amendment[0], defaults = {'proposer':amendment[0], 'status':amendment[1], 'link':amendment[2]})
                for transcript in related_transcripts_list:
                    b.transcript_set.update_or_create(name = transcript[0], defaults={'name':transcript[0], 'link':transcript[1]})
                for text in text_copies_list:
                    b.textcopy_set.update_or_create(name = text[0], defaults={'name':text[0], 'link':text[1]})
                for info in additional_info_list:
                    b.additionalinfo_set.update_or_create(name = info[0], defaults={'name':info[0], 'link':info[1]})
              
                
                
                print(introducer.name, bill_number, created)
        else: 
            print("No bills for", introducer.name)
        
        
def getDays():
    # This function gets all of the days from the dropdown list at nebraskalegislature.gov/bills
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
    #This function puts all of the bills that have been introduced over a specified range of days.
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

    
