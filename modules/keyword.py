# urus regex keyword dan append to spesific file
def keywordMatcher(rawfilename,keyword):
	with open(rawfilename, "r", encoding="utf-8") as file:
		while (line := file.readline()):
			print(line.strip())
	
