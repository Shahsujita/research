import re
import urllib.request
from bs4 import BeautifulSoup as soup
import os
import math

namesfile = open("nameOS.txt")
with open('nameOS.txt') as f:
    alist = f.read().splitlines()
    
#writes csv file
header="Political Party,Company,Position,Position in the Board,City,State,Zip,Date, Amount,Recipient,Party Category"+"\n"
file = open(os.path.expanduser("donorsopenS.csv"),"wb")
file.write(bytes(header, encoding="ascii",errors="ignore"))

#scrapes data for each page
i = 0
donor_data_saved=""
middleName = False
while i < len(alist):
	nameList = alist[i].split(",")
	Position = nameList[1]
	fullName = nameList[0].split(" ")
	if len(fullName) == 3:
		url = "https://beta.fec.gov/data/receipts/individual-contributions/?two_year_transaction_period=2016&contributor_name=" + fullName[0]+"+"+fullName[1]+"+"+fullName[2]+"&min_date=01%2F01%2F2015&max_date=12%2F31%2F2016"
		middleName = True
		print(url)
	else:
		url = "https://beta.fec.gov/data/receipts/individual-contributions/?two_year_transaction_period=2016&contributor_name=" + fullName[0]+"+"+fullName[1]+"&min_date=01%2F01%2F2015&max_date=12%2F31%2F2016"
		middleName = False
		print(url)

	uReq = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
	page_html = urllib.request.urlopen(uReq).read()
	print("whole page")
	print(page_html)
	uClient = urllib.request.urlopen(uReq)
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	#print(page_soup)
	results = page_soup.body.find_all('td', text="No data available in table")
	if results:
		break
	else:
		tables = page_soup.findChildern('table')
		# This will get the first (and only) table. Your page may have more.
		my_table = tables[0]
		# You can find children with multiple tags by passing a list of strings
		rows = my_table.findChildren(['th', 'tr'])
		for row in rows:
			cells = row.findChildren('td')
			for cell in cells:
				value = cell.string
				print ("The value in this cell is %s" % value)
		break
	
	
	

