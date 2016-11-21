from bills.models import Introducer, Bill
import requests
from bs4 import BeautifulSoup
import re

i = 1
introducers = {}

while i < 142:
    r = requests.get("http://nebraskalegislature.gov/bills/search_by_introducer.php?Introducer=%s" % str(i))
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    header = soup.find('h2').text
    split = header.split(',')
    name = re.match('.*?([A-Za-z]+)$', split[0]).group(1)
    if name != "Legislature":
        introducers[str(i)] = name
        print(name, str(i))
    else:
        continue
    i += 1

for key, value in introducers.items():
    obj, created = Introducer.objects.update_or_create(introducer_id=str(key), introducer_name = value, defaults = {'introducer_id' : str(key), 'introducer_name' : value})
   
   print(obj, created)
    
for object in Introducer.objects.all():
    id = str(object.introducer_id)
    print(id)
    r = requests.get("http://nebraskalegislature.gov/bills/search_by_introducer.php?Introducer=%s" % id)
    data = r.text
    soup = BeautifulSoup(data, "html.parser")
    
    table = soup.find('tbody')
    if table != None:
        bills = table.find_all('tr')
        bills_list = []
        for bill in bills:
            bill_name = bill.find_all('td')[3].text.strip()
            bill_link = bill.find_all('a')[0]['href']      
            bill_number = bill.find_all('a')[0].text 
            bill_id = re.match('.*?([0-9]+)$', bill_link).group(1)
            introduction_date = "2016-01-01"                      
            status = bill.find_all('td')[2].text.strip()
            object.bill_set.update_or_create(bill_id=bill_id, defaults = {'bill_name':bill_name, 'bill_number':bill_number, 'introduction_date':introduction_date, 'status':status})
    else:
        continue