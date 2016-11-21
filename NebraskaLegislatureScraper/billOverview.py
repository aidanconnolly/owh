#This script requests bill overview information from the Nebraska Legislature website and combines it into a csv. It requires a csv named "base.csv" to be in the same directory with the column names: Document, Primary Introducer, Status, Description and Date Introduced. The final csv is exported to the same directory as "bills.csv". An example page is here: http://nebraskalegislature.gov/bills/search_by_date.php?SessionDay=2016-01-06. 

import agate
import requests
import io
from datetime import datetime, date, timedelta

#This function creates a list of days to send to the website to request data.

def perdelta(start, end, delta):
    curr = start
    while curr < end:
        yield curr
        curr += delta
        
#This function gets the data from the website and merges it with the existing data in the bills table.        
def overview(sY, sM, sD, eY, eM, eD, delta):
    bills = agate.Table.from_csv("base.csv",column_types=[agate.Text(), agate.Text(), agate.Text(), agate.Text(), agate.Date()])
    
    print("List of dates:")
    for day in perdelta(date(sY, sM, sD), date(eY, eM, eD), timedelta(days=delta)):
        print("\t", day)
        with requests.Session() as s:
            day = str(day)
            csv = s.get("http://nebraskalegislature.gov/bills/search_by_date.php?SessionDay=%s&print=true" % day).content
            table = agate.Table.from_csv(io.StringIO(csv.decode('utf-8')), column_types=[agate.Text(), agate.Text(), agate.Text(), agate.Text()])

            table = table.compute([
                ('Date Introduced', agate.Formula(agate.Date(), lambda row: day % row))
            ])
            list = [bills, table]
            bills = agate.Table.merge(list)
            
    print("\n", len(bills.rows), "bills added.")
    bills.to_csv("bills.csv")

#These create the range of dates to request data. The end day is not inclusive. "Delta" is the number of days to jump. A value of 1 returns every day in the range.
startYear = 2016
startMonth = 1
startDay = 6
endYear = 2016
endMonth = 4
endDay = 21
delta = 1

overview(startYear, startMonth, startDay, endYear, endMonth, endDay, delta)