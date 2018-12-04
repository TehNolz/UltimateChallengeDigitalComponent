import json
import os

cards = {}
for file in os.listdir("data"):
	var = file.split("-")
	if var[0] == "card":
		id = var[1]+"-"+var[2].split(".")[0]
		if not var[1] in cards:
			cards[var[1]] = {}
		if id.split("-")[1] != "back":
			cards[var[1]][id] = {
				"file": file,
				"dice": False,
				"timer": False,
			}

with open('cardconfig.json', 'w') as outfile:
    json.dump(cards, outfile, indent=4)