class Killboard:
	import json
	import requests
	import operator
	import time

	# TODO: Seperate into functions, add verification earlier in main.
	def verify_url(self, tgt):
		# Status codes: 0 is ok, 1 is end of board, 2 is HTTP error
		temp = self.requests.get(tgt)
		try:
			temp.self.raise_for_status()
			# 404/error check
		except HTTPError:
			return 2
		if temp.text == '[]':
			# Checks to see if JSON is empty, in which case org does not exist
			return 1
		else:
			return 0

	def pull_kills(self):
		page = 1
		# As per Zkill API docs, default page is 1.
		print('Base URL: ' + self.url)
		print('Checking if killboard exists...')
		temp_url = self.url
		while 1:	
			temp_url = temp_url + 'page/' + str(page) + '/'
			if self.verify_URL(temp_url) != 0:
				break
			print('Now pulling from page' + page)
			buff = requests.get(temp_url)
			killbuffer = buff.json()
			for x in killbuffer:
					self.board[str(x['killmail_id'])] = x['zkb']['totalValue']
			page = page + 1

	def sort(self, modifer):
		# modifer of 1 will make order decending.
		self.board = sorted(self.board.items(), key=operator.itemgetter(1))
		if modifer == 1:
			self.board.reverse()
		# From a academic standpoint, this is cheating, but it works. This actually turns kills into a list of tuples.
		# TODO: Make actual fucking quicksort

	def make_url(self):
		# TODO: Make this only a sorting function
		# ID is a int, Type is 1 for corps, 2 for alliances
		baseURL = 'https://zkillboard.com/api/zkbOnly/kills/'
		if self.org_type == 1:
			self.url = baseURL + 'corporationID/' + str(self.org_ID) + '/'
		elif self.org_type == 2:
			self.url = baseURL + 'allianceID/' + str(self.org_ID) + '/'

	def to_file(self):
		final_url = 'http://zkillboard.com/kill/'
		out = input("What should the new file be named?")
		f = open(out, "w")
		for x in self.board:
			f.write('KILL ID: ' + str(x[0]) + ' | ' + 'ISK: ' + str(x[1]) + ' | URL: ' + final_url + str(x[0]) + '/ \n')
		f.close()
		print('Output file created as ' + out)

	def __init__(self):
		self.org_ID = 0
		self.org_type = 0
		self.url = ''
		while 1:
			self.org_ID = int(input("\nEnter the ID of the organization, must be corp or alliance \n"))
			while 1:
				self.org_type = int(input("\nEnter 1 if the organization is a corp, 2 if alliance \n"))
				if self.org_type == 1 or self.org_type == 2:
					break
				else:
					print("\nInvalid Identifier, try again\n")
			self.make_url()
			print(self.url)
			if self.verify_URL(self.url) == 0:
				break
			else:
				print('Invalid URL, from the top now...')
		self.board = {}
