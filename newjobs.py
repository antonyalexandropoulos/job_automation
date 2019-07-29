#!/usr/bin/python
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import os
import requests
from lxml import html
import json
import urllib.parse


queries = ["java","python","C#","software"]
with open('applied.txt','r')as f:
	content = f.readlines()
	applied = set(content)

def makelink(href):
	return "https://www.kariera.gr/"+ href

def makequery(s):
	return "https://www.kariera.gr/%CE%B8%CE%AD%CF%83%CE%B5%CE%B9%CF%82-%CE%B5%CF%81%CE%B3%CE%B1%CF%83%CE%AF%CE%B1%CF%82?utf8=%E2%9C%93&q=" +s+"&loc="
def apply(links):
	PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
	DRIVER_BIN = os.path.join(PROJECT_ROOT, "geckodriver")

	driver = webdriver.Firefox(executable_path = DRIVER_BIN)
	first = True
	for link in links:
		if link+'\n' in applied:continue
		driver.get(makelink(link))

		name = driver.find_element_by_id("firstname");
		name.click()
		name.send_keys("Antonios")

		lastname = driver.find_element_by_id("lastname");
		lastname.click()
		lastname.send_keys("Alexandropoulos")

		email = driver.find_element_by_id("contact_ApplicantEmail");
		email.click()
		email.send_keys("antonyalexandropoulos@gmail.com")

		cv = driver.find_element_by_id("upload_file");
		cv.send_keys("/Users/antonyalexandropoulos/jobsearch2019/curriculum-vitae (9).pdf")
		
		if first:
			cookies = driver.find_element_by_id("btn-cookie")
			cookies.click()
			first= False

		terms = driver.find_element_by_id("tac")
		terms.click()
		# SEND IS MISSING
		submit = driver.find_element_by_id("submit-unregistered")
		submit.click()

		with open('applied.txt','a') as f:
			f.write(link+'\n')

	driver.close()

joblinks = []
for q in queries:
	query = makequery(q)
	print (query)
	req = requests.get(query)
	webpage = html.fromstring(req.content)
	for x in webpage.xpath('//div[@id="jobs-content"]//a'):
		
		memo = eval(str(x.attrib))
		if memo.get('class') and memo['class']=='job-title':
			joblinks.append(memo['href'])
	

#for link in joblinks:print (urllib.parse.unquote(link)	)
final = set()
for link in joblinks:
	#print (link)
	try:
		req = requests.get(makelink(urllib.parse.unquote(link)))
		print (urllib.parse.unquote(link))
		webpage = html.fromstring(req.content)
		for x in webpage.xpath('//a'):
			#print( x)
			memo = eval(str(x.attrib))
			#for k,v in memo.items():print (k,v)
			if memo.get('class') and memo['class']=='btn btn-apply':
				if len(memo)<3:
					final.add(memo.get('href'))
					with open('oneclick.txt','a') as f:
						f.write(memo.get('href')+'\n')
				else:
					with open('multiclick.txt','a') as f:
						f.write(urllib.parse.unquote(link)+'\n')
			
			
	except:
		pass

for f in final:
	#print (f+'\n' in applied)
	print(makelink(f))
#exit()
apply(final)

#class="btn btn-apply"
#data-remodal-target

