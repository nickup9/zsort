import json
import requests
import operator
import time

def sort(orgID, orgType, output_name):
	#OrgID is a int, orgType is 1 for corps, 2 for alliances
	baseURL = 'https://zkillboard.com/api/zkbOnly/kills/'
	#for data pulling
	final_url = 'http://zkillboard.com/kill/'
	#for creating links to standard man-readable KMs

	page = 1
	#As per Zkill API docs, default page is 1.

	if orgType == 1:
		baseURL = baseURL + 'corporationID/' + str(orgID) + '/'
	elif orgType == 2:
		baseURL = baseURL + 'allianceID/' + str(orgID) + '/'
	else:
		print('Error: The wrong entity identifier was inputted/there was a error reading identifier')
		exit()
	#I feel like there are better ways to do this, but I can't be bothered to improve this ATM

	print('Base URL: ' + baseURL)
	print('Checking if killboard exists...')

	kills = dict()

	while 1:	
		url = baseURL + 'page/' + str(page) + '/'
		temp = requests.get(url)

		try:
			temp.raise_for_status()
			#404/error check
		except HTTPError:
			print('404 Error occured at page ' + str(page) + ' with URL ' + url + ' aborting...')
			break

		if temp.text == '[]':
			#Checks to see if JSON is empty, in which case org does not exist
			print('Done pulling...')
			break
		else:
			print('Pulling data from page ' + str(page))
			del temp

		buff = requests.get(url)
		killbuffer = buff.json()
		for x in killbuffer:
				kills[str(x['killmail_id'])] = x['zkb']['totalValue']
		page = page + 1



	kills = sorted(kills.items(), key=operator.itemgetter(1))
	#From a academic standpoint, this is cheating, but it works. This actually turns kills into a list of tuples.
	#TODO: Make actual fucking quicksort

	f = open(output_name, "w")
	for x in kills:
		f.write('KILL ID: ' + str(x[0]) + ' | ' + 'ISK: ' + str(x[1]) + ' | URL: ' + final_url + str(x[0]) + '/ \n')
	f.close()
	print('Output file created as ' + output_name)