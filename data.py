import os
import json
import globals

def loadData():
    imgIndex = globals.imgIndex
    fonts = globals.fonts
    
    #Load configuration files
    #Cardconfig
    
    if not os.path.exists('data/cardconfig.json'):
        raise MissingConfigException('', 'Unable to locate \'data\\cardconfig.json\'.')
    cardConfig = json.loads(open("data/cardconfig.json").read())
    
    #Userconfig
    if os.path.isfile("data/userconfig.json"):
        userConfig = json.loads(open("data/userconfig.json").read())
    else:
        userConfig = globals.userConfig
        globals.log.info("Config file missing, generating new blank...")
        with open('data/userconfig.json', 'w') as outfile:
            json.dump(userConfig, outfile, indent=4)
    globals.log.info("Loaded configs.")
    
    #Load all assets
    for file in os.listdir("data"):
        filetype = file.split(".")[1]
        name = file.split(".")[0]
        
        #Images
        if filetype == "png":
            imgIndex[name] = requestImage(file)
            
        #Fonts
        elif filetype == "vlw":
            fonts[file.split("-")[0]] = loadFont(file)
    
    #Wait for all images to finish loading.
    while True:
        var = True
        for img in imgIndex:
            imgWidth = imgIndex[img].width
            if imgWidth == 0:
                var = False
            elif imgWidth == -1:
                var = False
        if var:
            break
        
    globals.imgIndex = imgIndex
    globals.cardConfig = cardConfig
    globals.userConfig = userConfig
    
def saveData():
    userConfig = globals.userConfig
    with open('data/userconfig.json', 'w') as outfile:
        json.dump(userConfig, outfile, indent=4)

class MissingConfigException(Exception):
    def __init__(self, message, cause):
        self.message = message
        self.args = (message, cause)
    def __str__(self):
        return self.message
