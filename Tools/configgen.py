import json
import os

cards = {}
for file in os.listdir("..\data"):
	var = file.split("-")
	if var[0] == "card":
		id = file.split(".")[0]
		if not var[1] in cards:
			cards[var[1]] = {}
		if id.split("-")[2] != "back":
			cards[var[1]][id] = {
				"dice": False,
				"timer": False,
			}

with open('cardconfig.json', 'w') as outfile:
    json.dump(cards, outfile, indent=4)