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
		url = "http://www.opensecrets.org/donor-lookup/results?name=" + fullName[0]+"+"+fullName[1]+"+"+fullName[2]+"&page="
		middleName = True
	else:
		url = "http://www.opensecrets.org/donor-lookup/results?name=" + fullName[0]+"+"+fullName[1]+"&page="
		middleName = False

	uReq = urllib.request.Request(url+str(1), headers={'User-Agent': 'Mozilla/5.0'})
	page_html = urllib.request.urlopen(uReq).read()
	uClient = urllib.request.urlopen(uReq)
	uClient.close()
	page_soup = soup(page_html, "html.parser")
		
	#multiple_pages
	results = page_soup.findAll("p")[4].text
	numbers = results.split(" ")
	print("number=")
	print(numbers)
	if(numbers[0] == 'No'):
		line = nameList[0]+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+","+"-"+"\n"
		file.write(bytes(line, encoding="ascii",errors="ignore"))
		i += 1
		continue
		
	num1 = int(numbers[3])
	numbers[5] = numbers[5].replace(",", "")
	num2 = int(numbers[5])
	iters = 1
	if num2 > 50 :
		iters = math.ceil(num2/50)
	
	#iterate through all the pages 
	for j in range(1,iters+1):
		print(url+str(j))
		uReq = urllib.request.Request(url+str(j), headers={'User-Agent': 'Mozilla/5.0'})
		page_html = urllib.request.urlopen(uReq).read()
		uClient = urllib.request.urlopen(uReq)
		uClient.close()
		page_soup = soup(page_html, "html.parser") 
		for record in page_soup.findAll("tr"):
			nogetAddress = True # we did not get address yet
			nogetCompany = True
			nogetDate = True
			nogetAmount = True
			nogetRecipient = True
			line = ""
			companyName = ""
			donor_city = ""
			donor_state = ""
			donor_zip = ""
			Date = ""
			Amount = ""
			Recipient = ""
			Party = ""
			
			for data in record.findAll("td")[1:7]:
				donor_data_address = data.text.replace(",","")
				donor_data_address1 = donor_data_address.split()
				if middleName and nogetAddress and len(donor_data_address1) == 7:
					print("len 7 and middle nme")
					print(donor_data_address1)
					donor_city = donor_data_address1[4]
					donor_state = donor_data_address1[5]
					donor_zip = donor_data_address1[6]
					nogetAddress = False
				elif middleName and nogetAddress and len(donor_data_address1) == 8:
					print("len 8 and middle nme")
					print(donor_data_address1)
					donor_city = donor_data_address1[5]
					donor_state = donor_data_address1[6]
					donor_zip = donor_data_address1[7]
					nogetAddress = False
				elif middleName and nogetAddress and len(donor_data_address1) == 5:
					print("len 5 and middle nme")
					print(donor_data_address1)
					donor_city = '-'
					donor_state = donor_data_address1[3]
					donor_zip = donor_data_address1[4]
					nogetAddress = False
				elif middleName and nogetAddress and len(donor_data_address1) == 3:
					print("len 3 and middle nme")
					print(donor_data_address1)
					donor_city = '-'
					donor_state = '-'
					donor_zip = '-'
					nogetAddress = False
				elif nogetAddress:
					if len(donor_data_address1) == 2:
						print("len 2 and no middle nme")
						print(donor_data_address1)
						donor_city = "-"
						donor_state = "-"
						donor_zip = "-"
						nogetAddress = False
					elif len(donor_data_address1) == 4:
						print("len 4 and no middle nme")
						print(donor_data_address1)
						donor_city = donor_data_address1[2]
						donor_state = donor_data_address1[3]
						donor_zip = "-"
						nogetAddress = False
					elif len(donor_data_address1) == 5:
						nogetAddress = False
						if not len(donor_data_address1[2]) == 1:
							donor_city = donor_data_address1[2]
							donor_state = donor_data_address1[3]
							donor_zip = donor_data_address1[4]
						else:
							print("len 5 and no middle nme")
							print(donor_data_address1)
							donor_city = donor_data_address1[3]
							donor_state = donor_data_address1[4]
							donor_zip = "-"
					elif len(donor_data_address1) == 8:
						print("len 8 and no middle nme")
						print(donor_data_address1)
						donor_city = donor_data_address1[5]
						donor_state = donor_data_address1[6]
						donor_zip = donor_data_address1[7]
						nogetAddress = False
					elif len(donor_data_address1) == 3:
						print("len 3 and no middle nme")
						print(donor_data_address1)
						donor_city = "-"
						donor_state = "-"
						donor_zip = "-"
						nogetAddress = False
					else:
						print("len 6 and no middle nme")
						print(donor_data_address1)
						donor_city = donor_data_address1[3]
						donor_state = donor_data_address1[4]
						donor_zip = donor_data_address1[5]
						nogetAddress = False
				elif nogetCompany:
					donor_data_address = data.text.replace(",","")
					companyName = donor_data_address
					nogetCompany = False
				elif nogetDate:
					Date = data.text.replace(",","")
					nogetDate = False
				elif nogetAmount:
					Amount = data.text.replace(",","")
					nogetAmount = False
				else:
					Recipient = data.text.replace(",","")
					if len(Recipient.split("(")) == 2:
						print(Recipient.split("("))
						Party = Recipient.split("(")[1][:-1]
						Recipient = Recipient.split("(")[0][:-1]
					else:
						Party = "-"
					nogetRecipient = False
				line = nameList[0]+","+companyName+","+"-"+","+Position+","+donor_city+","+donor_state+","+donor_zip+","+Date+","+Amount+","+Recipient+","+Party+"\n"
				print(line)
			file.write(bytes(line, encoding="ascii",errors="ignore"))
	i += 1
file.close()

