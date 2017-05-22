from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import os

namesfile = open("names.txt")
with open('names.txt') as f:
    alist = f.read().splitlines()
print(alist)


#scrapes data for each page
i = 0
donor_data_saved=""
while i < len(alist):
	nameList = alist[i].split(" ")
	url = "http://www.campaignmoney.com/finance.asp?type=in&cycle=16&criteria=" + nameList[1]+"&fname="+nameList[0]
	#http://www.campaignmoney.com/finance.asp?pg=2&type=in&criteria=griffin&ra=12278352&rc=129&prevpage=1&cycle=16&fname=kenneth
	print(url)
	i += 1
	uClient = uReq(url)
	page_html = uClient.read()
	uClient.close()
	page_soup = soup(page_html, "html.parser")
	for record in page_soup.findAll("tr",{"class":["GridOdd","GridEven"]}):
		donor_data=""
		for data in record.findAll("td"):
			donor_data = donor_data + "," + data.text.replace(",","")
		donor_data_saved = donor_data_saved + "\n" + alist[i-1] + "," + donor_data[1:]

#writes csv file
header="name,contributed,party,amount,date"+"\n"
file = open(os.path.expanduser("donors.csv"),"wb")
file.write(bytes(header, encoding="ascii",errors="ignore"))
file.write(bytes(donor_data_saved, encoding="ascii",errors="ignore"))


