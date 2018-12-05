import logging

#Data
imgIndex = {}
cardConfig = {}
fonts = {}

#Scale
baseScale = 1.0

#Settings
gameconfig = {
    "useDecks": {
        "base",
        "expansion1",
        "expansion2"
    }
}

#Menus
currentMenu = "mainmenu"

#Misc
logging.basicConfig(level=logging.NOTSET)
log = logging.getLogger("LOG")
