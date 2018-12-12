import os
import json
import globals

def loadData():
    imgIndex = globals.imgIndex
    fonts = globals.fonts
    
    #Load configuration files
    #Cardconfig
    cardConfig = json.loads(open("cardconfig.json").read())
    
    #Userconfig
    if os.path.isfile("userconfig.json"):
        userConfig = json.loads(open("userconfig.json").read())
    else:
        userConfig = globals.userConfig
        with open('userconfig.json', 'w') as outfile:
            json.dump(userConfig, outfile, indent=4)
    
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
    with open('userconfig.json', 'w') as outfile:
        json.dump(userConfig, outfile, indent=4)
        
