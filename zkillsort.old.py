import json
import requests
import operator
import time

corpID = 0
allianceID = 448511760
page = 1
#As per API docs, default page is 1.

# Update manually, only use one. Example is for Dark Taboo, alliance. Program checks corp first.


baseURL = 'https://zkillboard.com/api/zkbOnly/kills/'
#for data pulling
final_url = 'http://zkillboard.com/kill/'
#for creating links to standard man-readable KMs
if corpID != 0:
	baseURL = baseURL + 'corporationID/' + str(corpID) + '/'
elif allianceID != 0:
	baseURL = baseURL + 'allianceID/' + str(allianceID) + '/'
else:
	print('No org ID was inputted, please try again')
	exit()
#Yes there are better ways to do this, yes, I can't be bothered to improve this ATM

print('Base URL: ' + baseURL)
print('Checking if killboard exists...')

kills = dict()

while 1:	
	url = baseURL + 'page/' + str(page) + '/'
	temp = requests.get(url)
	if temp.text == '[]' or temp.raise_for_status() == 0: #We need to have raise for status try to equal something, I think. Dunno if I can just leave it in 
		#there by itself. Also, raising for status buff (or any Requests object we want to pull data from) fucks up everything, dunno why.
		#Checks to see if JSON is empty, in which case org does not exist
		print('Done pulling')
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
#From a academic standpoint, this is cheating, but it works

f = open("sortresults.txt", "w")
for x in kills:
	f.write('KILL ID: ' + str(x[0]) + ' | ' + 'ISK: ' + str(x[1]) + ' | URL: ' + final_url + str(x[0]) + '/ \n')
f.close()
print('Done')