import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from sqlite3 import *

def get_url(search_term):
	template='https://www.amazon.in/s?k={}&crid=1AY5YVYRQ6DH9&sprefix=ultrawide+m%2Caps%2C203&ref=nb_sb_ss_ts-doa-p_2_11'
	search_term=search_term.replace('','')
	url=template.format(search_term)
	url+='&page={}'
	return url

def extract_record(item):
	atag=item.h2.a
	desc=atag.text.strip()
	url="https://www.amazon.in/"+ atag.get('href')
	try:
		price_parent=item.find('span','a-price')
		price=price_parent.find('span','a-offscreen').text.strip()
	except AttributeError:
		return
	try:
		rating=item.i.text
	except AttributeError:
		rating=''
	
	result=(desc,price,rating)
	return result
	

def main(search_term):
	driver=webdriver.Firefox()
	records=[]
	url=get_url(search_term)
	for page in range(1,3):
		driver.get(url.format(page))
		soup=BeautifulSoup(driver.page_source,"html.parser")
		results=soup.find_all('div',{'data-component-type':'s-search-result'})
		for item in results:
			record=extract_record(item)
			if record:
				records.append(record)
	print(records)
	driver.close()
	
	

	with open('result.csv','w',newline='',encoding='utf-8')as f:
		writer=csv.writer(f)
		writer.writerow(['Item Description','Price','Rating'])
		writer.writerows(records)

i1=input("Enter the Item Name you want to Scrape From Amazon --> ")
main(i1)
print("#################      ",i1.capitalize(),"Done Scraping Successfully    #########################")
	
