import re
import json
import requests

red = "\033[32m"
endred = "\033[32m"+"\033[0m"


def statusUrlFetcher(source, filename):
	print("fetching status url..")
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			string = line.strip()
			templist = list(string.split())
			try:
				string = templist[4]+"  "+templist[2]
			except:
				string = templist[2]
			# outfile.write(string )
			outfile.write(string + "\n")


def urlFetcher(source, filename):
	print("fetching url..")
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			string = line.strip()
			templist = list(string.split())
			string = templist[2]
			# outfile.write(string )
			outfile.write(string + "\n")


def statusBypassFetcher(source, filename):
	print("fetching bypass url..")
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			string = line.strip()
			templist = list(string.split())
			string = templist[4]+"  "+"https://web.archive.org/web/" + \
			    templist[1]+"/"+templist[2]
			# outfile.write(string )
			if templist[4] == "200":
				outfile.write(string + "\n")


def statusInsert(keyword1, keyword2sens, keyword3, keyword4sens,	keyword_status):
	for x in keyword1:
		keyword_status["nonsens"][x] = 0
	for x in keyword2sens:
		keyword_status["sens"][x] = 0
	for x in keyword3:
		keyword_status["nonsens"][x] = 0
	for x in keyword4sens:
		keyword_status["sens"][x] = 0
	return keyword_status


def commonKeywordFetcher(source, filename, keyword, keyword_status):
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			target = line.strip()
			for x in keyword:
				if re.search(re.escape(x), target):
					outfile.write(target + "\n")
					keyword_status["sens"][x] = 1
	return keyword_status


def commonNonSensKeywordFetcher(source, filename, keyword, keyword_status):
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			target = line.strip()
			for x in keyword:
				if re.search(re.escape(x), target, re.IGNORECASE):
					outfile.write(target + "\n")
					keyword_status["nonsens"][x] = 1
	return keyword_status


def userKeywordFetcher(source, filename, keyword, keyword_status):
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			target = line.strip()
			for x in keyword:
				if re.search(re.escape(x), target):
					outfile.write(target + "\n")
					keyword_status["sens"][x] = 1
	return keyword_status


def userNonSensKeywordFetcher(source, filename, keyword, keyword_status):
	with open(source, "r", encoding="utf-8") as file, open(filename, "w", encoding="utf-8") as outfile:
		while (line := file.readline()):
			target = line.strip()
			for x in keyword:
				if re.search(re.escape(x), target, re.IGNORECASE):
					outfile.write(target + "\n")
					keyword_status["nonsens"][x] = 1
	return keyword_status


def getKeywordNonSensFromStatus(source, keyword):
	with open(source, "r", encoding="utf-8") as file:
		while (line := file.readline()):
			target = line.strip()
			if re.search(re.escape(keyword), target, re.IGNORECASE):
					print(target)


def getKeywordSensFromStatus(source, keyword):
	with open(source, "r", encoding="utf-8") as file:
		while (line := file.readline()):
			target = line.strip()
			if re.search(re.escape(keyword), target):
					print(target)


def writeStatusFound(filename, keyword_status):
	with open(filename, "w", encoding="utf-8") as json_file:
		json.dump(keyword_status, json_file, indent=4)


def showStatus(filename):
	with open(filename, "r", encoding="utf-8") as json_file:
		data = json.load(json_file)
		print("== sensitive keyword ==")
		for key, value in data["sens"].items():
			if value == 0:
				print("\033[31m"+key+"\033[31m")
			else:
				print("\033[32m"+key+"\033[32m")
		print("\n\n\033[0m== non-sensitive keyword ==")
		for key, value in data["nonsens"].items():
			if value == 0:
				print("\033[31m"+key+"\033[31m")
			else:
				print("\033[32m"+key+"\033[32m")
		print("\033[0m")
		print("== end result ==")


def checkStatusUrl(url):
	try:
		  response = requests.get(url)
		  # Print only the HTTP status code
		  print(response.status_code, " --response from internet")
	except requests.exceptions.RequestException as e:
		  print(f"Error: {e}")  # Handle request errors


def getUrlFromFile(source, url):
	with open(source, "r", encoding="utf-8") as file:
		# print('tes')
		while (line := file.readline()):
			target = line.strip()
			if re.search(re.escape(url), target, re.IGNORECASE):
					print(target)


def getUrlRegexFromFile(source, url):
	with open(source, "r", encoding="utf-8") as file:
		# print('tes')
		while (line := file.readline()):
			target = line.strip()
			if re.search(url, target, re.IGNORECASE):
					print(target)


def matchBypass(source, url):
	checkStatusUrl(url)
	getUrlFromFile(source, url)


def subdomainFetch(source, url):
	with open(source, "r", encoding="utf-8") as file, open(url, "w", encoding="utf-8") as outfile:
		# print('tes')
		tempdomain = ""
		tempdomainset = set()
		while (line := file.readline()):
			target = line.strip()
			itert = 0
			index = 0
			# print("mulai",target,itert,index)
			for x in target:
				index += 1
				if x == "/":
					itert += 1
					# print(x,itert,index)
				if itert == 3:

						tempdomain = target[:index]
						tempdomainset.add(tempdomain)
						# outfile.write(tempdomain + "\n")
					# print("aw",target[:index],index,itert)
						break
		for x in tempdomainset:
			outfile.write(x + "\n")
def subdomainOnlyFetch(source,url):
	with open(source, "r", encoding="utf-8") as file,open(url, "w", encoding="utf-8") as outfile:
		#print('tes')
		tempdomain=""
		tempdomainset= set()
		while (line := file.readline()):
			target=line.strip()
			itert=0
			index=0
			start=0
			findsec=0
			#print("mulai",target,itert,index)
			for x in target:
				index+=1
				if x=="/":
					itert+=1
					#print(x,itert,index)
				if itert==2 and findsec==0:
					start=index
					findsec=1
				if itert==3:
					
						tempdomain=target[start:index-1]
						tempdomainset.add(tempdomain)
						#outfile.write(tempdomain + "\n")
						print("aw",tempdomain,start,index-1)
						break				
		for x in tempdomainset:
			outfile.write(x + "\n")
def getSubdomains(source):
	with open(source, "r", encoding="utf-8") as file:
		while (line := file.readline()):
			target=line.strip()
			print(target)



	
