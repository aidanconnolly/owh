import requests
from bs4 import BeautifulSoup

def billInfo(documentId):
    #------------------------------------------------------------#
    #Data Acquisition
    #This goes and requests the bill information from the Nebraska Legislature website and parses it with BeautifulSoup
    
    print('Getting html structure...')
    r = requests.get("http://nebraskalegislature.gov/bills/view_bill.php?DocumentID=%s" % str(documentId))
    data = r.text
    
    print('Parsing html structure...')
    soup = BeautifulSoup(data, "html.parser")
    
    #------------------------------------------------------------#
    #Bill Name
    #This gets the bill name from the h2 tag on the page.
    
    print('\tGetting bill name...')
    bill_name = soup.find('h2').text
    
    #------------------------------------------------------------#
    #Bill Info
    #This gets the bill info from the top row of the page. The three lists of info are the only lists with the class 'list-unstyled'. This includes document info, text copies and additional info.
    
    print('\tGetting bill info...')
    bill_info = soup.find_all('ul', class_='list-unstyled')
    
    #Document Info
    #Document Info is the first list with the class 'list-unstyled'. In contains the introducer and an introduction date. Both have links to search by that information.
    
    print('\t\tGetting document info...')
    document_info = bill_info[0].find_all('li')
    
    #Introducer
    
    introducer = document_info[0]
    introducer_text = introducer.find('a').text
    introducer_link = introducer.find('a')['href']
    
    #Introduction Date
    
    introduction_date = document_info[1]
    introduction_date_text = introduction_date.text
    introduction_date_link = introduction_date.find('a')['href']
    
    #Text Copies
    #Text Copies is the second list with the class 'list-unstyled'. It has different copies of the bill. The entries are links to PDFs. This finds all of the entries and loops through them, adding the information to the text_copies_list.
    
    print('\t\tGetting text copies...')
    text_copies = bill_info[1].find_all('li')
    text_copies_list = []
    for text_copy in text_copies:
        text_copy_text = text_copy.text
        text_copy_link = text_copy.find('a')['href']
        text_copies_list.append((text_copy_text, text_copy_link))
        
    #Additional Info
    #Additional Info is the third list with the class 'list-unstyled'. It contains different links to different items, which can be different formats. This finds the entries and loops through them, adding the information to the additional_info_list.
    
    print('\t\tGetting additional info...')
    additional_info = bill_info[2].find_all('li')
    additional_info_list = []
    for additional in additional_info:
        additional_text = additional.text
        additional_link = additional.find('a')['href']
        additional_info_list.append((additional_text, additional_link))
        
    #------------------------------------------------------------#
    #History
    #History shows all of the logged events associated with this bill. Each entry has a date, an action and a journal page link. This loops through the entries and adds the information to the history_list.
    
    print('\tGetting history...')
    history = soup.find_all('div', class_="col-sm-8")[1].find('tbody').find_all('tr')
    history_list = []
    for history_item in history:
        history_item_info = history_item.find_all('td')
        history_item_date = history_item_info[0].text
        history_item_action = history_item_info[1].text
        history_item_link = history_item_info[2].find('a')['href']
        history_item_link_text = history_item_info[2].find('a').text
        history_list.append((history_item_date, history_item_action, history_item_link_text, history_item_link))
        
    #------------------------------------------------------------#
    #Proposed Amendments
    #Proposed By Priority deals with proposed amendments. Information includes who proposed the amendment, a link to the amendment and its current status. This loops through the entries, adding them to the proposed_amendments_list. The odd entries are the amendments and links; the even entries are the statuses.
    
    print('\tGetting proposed amendments...')
    proposed_amendments = related_transcripts = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[1].find_all('tr')
    proposed_amendments_list = []
    for proposed_amendment in proposed_amendments:
            proposed_amendment_text = proposed_amendment.text.strip().split('\n\n\n')
            proposed_amendment_proposer = proposed_amendment_text[0]
            proposed_amendment_status = proposed_amendment_text[1].strip()
            proposed_amendment_link = proposed_amendment.find('a')['href']
            proposed_amendments_list.append((proposed_amendment_proposer, proposed_amendment_status, proposed_amendment_link))
                                                                         
    #------------------------------------------------------------#
    #Related Transcripts
    #Related Transcripts includes entries with links to transcripts that mention the bill. This loops through the entries and adds them to the related_transcripts_list.
    
    print('\tGetting related transcripts...')
    related_transcripts = soup.find_all('div', class_="col-sm-4")[3].find_all('table')[2].find_all('td')
    related_transcripts_list = []
    for related_transcript in related_transcripts:
        related_transcript_text = related_transcript.text
        related_transcript_link = related_transcript.find('a')['href']
        related_transcripts_list.append((related_transcript_text, related_transcript_link))
        
    #------------------------------------------------------------#
    #Pre-output
    #This prints the information to the screen for the user to review.
    print("Bill Name:", bill_name)
    print("Bill Introducer:", introducer_text)
    print("Bill Introduction Date:", introduction_date_text)
    if len(text_copies_list) > 0:
        print("Text Copies:")
        for entry in text_copies_list:
            print("\t", entry[0])
    else:
        print("No text copies.")
    
    if len(additional_info_list) > 0:
        print("Additional Info:")
        for entry in additional_info_list:
            print("\t", entry[0])
    else:
        print("No additional info.")
    
    if len(history_list) > 0:
        print("History:")
        for entry in history_list:
            print("\t", entry[0], "\t", entry[1], "\t", entry[2])
    else:
        print("No history.")
   
    if len(proposed_amendments_list) > 0:
        print("Proposed Amendments:")
        for entry in proposed_amendments_list:
            print("\t", entry[0], "\t", entry[1])
    else:
        print("No proposed amendments.")
    
    if len(related_transcripts_list) > 0:
        print("Related Transcripts:")
        for entry in related_transcripts_list:
            print("\t", entry[0])
    else:
        print("No related transcripts.")
        
billInfo(24440)
            