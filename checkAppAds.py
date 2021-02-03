import re
import requests
import csv
import json
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

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

def getAppAdsFile(filename):
	with open('app-ads.txt', 'r') as file:
		return [line.rstrip('\n').lower() for line in file]

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
	if 'results' not in response or not response["results"]:
		print(str(bundle) + " is not in store")
	else:
		result = response["results"][0]
		if 'sellerUrl' in result:
			sellerDomain = result["sellerUrl"]
	return sellerDomain

def getAppAdsInfo(domain):
	# print(domain)
	hasAppAdsTxt = True
	appAdsTxt = ""
	try:
		appAdsURL = urljoin(domain, '/app-ads.txt')
		r = requests.get(url = appAdsURL)
		appAdsTxt = r.text.replace(" ", "").lower()
	except:
		hasAppAdsTxt = False
	return hasAppAdsTxt, appAdsTxt

def getMissingValues(sspAppAdsEntries, appAdsTxt):
	missingValues = []
	for entry in sspAppAdsEntries:
		if entry not in appAdsTxt:
			missingValues.append(entry)
	return missingValues

appsList = getAppsFromCsv('apps.csv')
sspAppAdsEntries = getAppAdsFile('app-ads.txt')

with open('appAds.csv', 'w', newline='') as csvfile:
	csvWriter = csv.writer(csvfile, delimiter=';')
	csvWriter.writerow(['App Bundle', 'Platform', 'App Domain', 'Has app-ads.txt?', 'Missing entries'])
	domainStr = ''
	missingValuesTxt = ''
	for app in appsList:
		print('Fetching info for app: ' + app[1])
		if app[0] == 'ios':
			domain = getIOSAppDomain(app[1])
			domainStr = urlparse(domain).netloc
		else:
			domain = getAndroidAppDomain(app[1])
			domainStr = urlparse(domain).netloc
		if not domainStr:
			domainStr = 'NO DOMAIN' 
		hasAppAdsTxt, appAdsTxt = getAppAdsInfo(domain)
		if hasAppAdsTxt:
			missingValues = getMissingValues(sspAppAdsEntries, appAdsTxt)
			missingValuesTxt = '\n'.join([str(elem) for elem in missingValues]) 
		csvWriter.writerow([app[1], app[0], domainStr, hasAppAdsTxt, missingValuesTxt])

