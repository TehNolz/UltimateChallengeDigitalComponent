import json

cards = {"challengeCards": {}}
for i in range(1, 51):
	cards["challengeCards"][i] = {
		"file": "card-challenge-"+str(i)+".png",
		"dice": False,
		"timer": False,
		"skippable": True,
	}

cards["challengeCards"]["back"] = {
	"file": "card-challenge-back.png",
}

with open('cardconfig.json', 'w') as outfile:
    json.dump(cards, outfile, indent=4)