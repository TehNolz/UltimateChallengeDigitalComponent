from util import *
import logging

#Data
imgIndex = {}
cardConfig = {}
userConfig = {
    "players": {
        1: None,
        2: None,
        3: None,
        4: None,
        5: None,
        6: None,
    },
    "settings": {
        "useDecks": [
            "base",
            "expansion1",
            "expansion2"
        ]
    }
}
fonts = {}

#Scale
baseScale = 1.0
baseScaleXY = Vector2(1,1)

# Base screen size
# Probably not implemented everywhere, but not my problem >:(
baseScreenSize = Vector2(1133, 600)

#Menus
currentMenu = "mainMenu"

# Colors
backgroundColor = color(180)

#Misc
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger("LOG")
playerCount = 0

#Text boxes
activeTextBox = None
textBoxDict = {"global": []}
