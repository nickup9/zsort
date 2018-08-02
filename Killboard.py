class Killboard:
	import json
	import requests
	import operator
	import time

	#TODO: Seperate into functions, add verification earlier in main.

	def __init__(self):
		while 1:
			self.org_ID = int(input("\nEnter the ID of the organization, must be corp or alliance \n"))
			while 1:
				self.org_type = int(input("\nEnter 1 if the organization is a corp, 2 if alliance \n"))
				if org_type == 1 or org_type == 2
					break
				else
					print("\nInvalid Identifier, try again\n")
			self.url = get_url()
				if verify_URL(url) == 0
					break
				else
					print('Invalid URL, from the top now...')
		self.board = {}

	def pull_kills():
		page = 1
		#As per Zkill API docs, default page is 1.
		print('Base URL: ' + url)
		print('Checking if killboard exists...')
		temp_url = url
		while 1:	
			temp_url = temp_url + 'page/' + str(page) + '/'
			if verify_URL(temp_url) != 0
				break
			buff = requests.get(temp_url)
			killbuffer = buff.json()
			for x in killbuffer:
					board[str(x['killmail_id'])] = x['zkb']['totalValue']
			page = page + 1

	def sort(modifer):
		#modifer of 1 will make order decending.
		board = sorted(board.items(), key=operator.itemgetter(1))
		if modifer == 1:
			board.reverse()
		#From a academic standpoint, this is cheating, but it works. This actually turns kills into a list of tuples.
		#TODO: Make actual fucking quicksort

	def get_url():
		#TODO: Make this only a sorting function
		#ID is a int, Type is 1 for corps, 2 for alliances
		baseURL = 'https://zkillboard.com/api/zkbOnly/kills/'
		if org_type == 1:
			baseURL = baseURL + 'corporationID/' + str(org_ID) + '/'
		elif org_type == 2:
			baseURL = baseURL + 'allianceID/' + str(org_ID) + '/'
		else:
			print('Error: The wrong entity identifier was inputted/there was a error reading identifier')
		#I feel like there are better ways to do this, but I can't be bothered to improve this ATM

	def to_file(out):
		final_url = 'http://zkillboard.com/kill/'
		f = open(out, "w")
		for x in board:
			f.write('KILL ID: ' + str(x[0]) + ' | ' + 'ISK: ' + str(x[1]) + ' | URL: ' + final_url + str(x[0]) + '/ \n')
		f.close()
		print('Output file created as ' + out)

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