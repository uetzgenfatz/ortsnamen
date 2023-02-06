#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Simple script that scrapes GeoHack (via Wikipedia) for geo-coordinates of a given list of place names (input: .csv)
# Oliver Schallert, 2021
# bugfixes (full compatibility with Unicode input) by Alexander Dröge and Phillip Alday
# only compatible with Python 3

import re
from bs4 import BeautifulSoup
import urllib.error
import urllib.parse
import urllib.request
import csv
import ssl

def getCoords():
	ssl._create_default_https_context = ssl._create_unverified_context

	url="https://de.wikipedia.org/wiki/"

	t = open("koordinaten.csv", mode='wt', encoding='utf-8-sig')
	print("Ort"+";"+"X"+";"+"Y", file=t)

	with open("orte.csv", mode='r', encoding='utf-8-sig') as csvfile:
		f = csv.DictReader(csvfile)
		for row in f:
			try:
				ort = row['Ort']
				ort_url = urllib.parse.quote(ort.encode('UTF-8'))
				link = url+ort_url
				x = urllib.request.urlopen(link)
				soup = BeautifulSoup(x.read(), "html.parser")
				hoi = soup.find('span', {'class' : 'latitude'})
				hai = soup.find('span', {'class' : 'longitude'})
				long = str(hoi.get_text())
				lat = str(hai.get_text())
				print(ort+";"+lat+";"+long, file=t)
			except (AttributeError, urllib.error.HTTPError):
				lat = 'NA'
				long = 'NA'
				print(ort+";"+lat+";"+long, file=t)

	t.close()

if __name__ == '__main__':
	getCoords()