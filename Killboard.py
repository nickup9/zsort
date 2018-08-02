class Killboard:
	import json
	import requests
	import operator
	import time

	#TODO: Seperate into functions, add verification earlier in main.

	def __init__(self, ID, Type):
		self.org_ID = ID
		self.org_type = Type
		board = dict()

	def pull_kills(ID, Type):
		#TODO: Make this only a sorting function
		#ID is a int, Type is 1 for corps, 2 for alliances
		baseURL = 'https://zkillboard.com/api/zkbOnly/kills/'
		#for data pulling
		final_url = 'http://zkillboard.com/kill/'
		#for creating links to standard man-readable KMs

		page = 1
		#As per Zkill API docs, default page is 1.

		if Type == 1:
			baseURL = baseURL + 'corporationID/' + str(ID) + '/'
		elif Type == 2:
			baseURL = baseURL + 'allianceID/' + str(ID) + '/'
		else:
			print('Error: The wrong entity identifier was inputted/there was a error reading identifier')
			exit()
		#I feel like there are better ways to do this, but I can't be bothered to improve this ATM

		print('Base URL: ' + baseURL)
		print('Checking if killboard exists...')

		while 1:	
			url = baseURL + 'page/' + str(page) + '/'
			verify_URL(url)
			buff = requests.get(url)
			killbuffer = buff.json()
			for x in killbuffer:
					kills[str(x['killmail_id'])] = x['zkb']['totalValue']
			page = page + 1

		return kills
		#End of function here

	def sort(modifer):
		#modifer of 1 will make order decending.
		board = sorted(board.items(), key=operator.itemgetter(1))
		if modifer == 1:
			board.reverse()
		#From a academic standpoint, this is cheating, but it works. This actually turns kills into a list of tuples.
		#TODO: Make actual fucking quicksort

	def to_file(kills):
		f = open(output_name, "w")
		for x in kills:
			f.write('KILL ID: ' + str(x[0]) + ' | ' + 'ISK: ' + str(x[1]) + ' | URL: ' + final_url + str(x[0]) + '/ \n')
		f.close()
		print('Output file created as ' + output_name)

	def verify_URL(tgt):
		#Status codes: 0 is ok, 1 is end of board, 2 is HTTP error
		temp = requests.get(tgt)
		try:
			temp.raise_for_status()
			#404/error check
		except HTTPError:
			return 2
		if temp.text == '[]':
			#Checks to see if JSON is empty, in which case org does not exist
			return 1
		else:
			return 0