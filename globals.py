from util import *
import logging

#Data
imgIndex = {}
cardConfig = {}
userConfig = {
    "players": [
        None,
        None,
        None,
        None,
        None,
        None,
    ],
    "settings": {
        "useDecks": [
            "base",
            "expansion1",
            "expansion2"
        ],
        "bg_select": 'Blue',
        "primary_color": color(50, 230, 230),
        "objectAnims_OnOff": True,
        "anims_OnOff": True,
        "font": 'Open Sans',
        "enable_debug_console": False
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

# Background
backgroundImgName = 'background'
backgroundImg = None

#Misc
logging.basicConfig(filename='ucdc_app.log', level=logging.NOTSET, format='[%(asctime)s][%(name)s:%(levelname)s] %(message)s',  filemode='w+', datefmt='%X')
log = logging.getLogger("LOG")
playerCount = 0
font = None

#Text boxes
activeTextBox = None
textBoxDict = {"global": []}
