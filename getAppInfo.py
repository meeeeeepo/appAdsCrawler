import re
import requests
import csv
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse

appsList = []
androidURL = 'https://play.google.com/store/apps/details?id='
iOSURL = 'http://itunes.apple.com/lookup?id='

def getAppsFromCsv(fileName):
	dict = []
	with open('apps.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		line_count = 0
		for row in csv_reader:
			dict.append(row)
	return dict

def getAndroidAppDomain(bundle):
	storeURL = androidURL + str(bundle)
	r = requests.get(url = storeURL)
	htmlResponse = r.text
	soup = BeautifulSoup(htmlResponse, "html.parser")
	result = soup.findAll("a")
	sellerDomain = ''
	for element in result:
		if element.string == 'Visit website':
			sellerDomain = element['href']
			break
	return sellerDomain

def getIOSAppDomain(bundle):
	storeURL = iOSURL + str(bundle)
	r = requests.get(url = storeURL)
	response = json.loads(r.content)
	sellerDomain = ''
	if not response["results"]:
		print(str(bundle) + " is not in store")
	else:
		result = response["results"][0]
		if 'sellerUrl' in result:
			sellerDomain = result["sellerUrl"]
	return sellerDomain


appsList = getAppsFromCsv('apps.csv')
with open('domains.csv', 'w', newline='') as csvfile:
	csvWriter = csv.writer(csvfile, delimiter=',', quotechar=',', quoting=csv.QUOTE_MINIMAL)
	for app in appsList:
		if app[0] == 'ios':
			domain = urlparse(getIOSAppDomain(app[1])).netloc
			csvWriter.writerow([app[1], domain])
		else:
			domain = urlparse(getAndroidAppDomain(app[1])).netloc
			csvWriter.writerow([app[1], domain])

