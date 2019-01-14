import os
import json
import globals
from util import getMostRecentCall

loadingAssets = False
totalRequests = 0
_totalRequests = 0
loadStart = 0
assetNames = dict()
def loadData(firstLoad=False):
    global loadStart
    global loadingAssets
    global totalRequests
    global _totalRequests
    global assetNames
    
    imgIndex = globals.imgIndex
    fonts = globals.fonts
    
    #Wait for all images to finish loading.
    if firstLoad and not loadingAssets:
        loadStart = millis()
    if firstLoad and loadingAssets:
        # Raise an exception if an asset takes more than 2000 ms to load.
        # This usually means a memory overflow has ocurred.
        if millis() - loadStart > 2000:
            raise BufferError('Asset loading timed out. (>2000ms)')
        
        lastLoadedAsset = None
        finishedRequests = 0
        _finishedRequests = 0
        for img in imgIndex:
            imgWidth = imgIndex[img].width
            if imgWidth == 0:
                var = False
            elif imgWidth == -1:
                var = False
            else:
                loadStart = millis()
                finishedRequests += os.path.getsize(assetNames[img])
                _finishedRequests += 1
        if totalRequests == finishedRequests or _totalRequests == _finishedRequests:
            globals.imgIndex = imgIndex
            loadingAssets = False
        return totalRequests, finishedRequests, _totalRequests, _finishedRequests
    else:
        totalRequests = 0
    
    #Load configuration files
    #Cardconfig

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
    for file in [_ for _ in os.listdir("data") if os.path.isfile('data\\'+_)]:
        filetype = file.split(".")[1]
        name = file.split(".")[0]
        
        #Images
        if filetype == "png":
            totalRequests += os.path.getsize(os.path.realpath('data\\'+file))
            _totalRequests += 1
            imgIndex[name] = requestImage(file)
            assetNames[name] = os.path.realpath('data\\'+file)
            
        #Fonts
        elif filetype == "vlw":
            fonts[file.split("-")[0]] = loadFont(file)

    loadingAssets = True
    globals.cardConfig = cardConfig
    globals.userConfig = userConfig
    return totalRequests, 0 , _totalRequests, 0
    
def saveData():
    import time
    saveStart = time.clock()
    userConfig = globals.userConfig
    with open('data/userconfig.json', 'w') as outfile:
        json.dump(userConfig, outfile, indent=4)
    globals.log.info('Saved settings.\t['+str(int((time.clock()-saveStart)*10**6))+' us]')
    globals.log.debug(u'\u2514\u2500 Call from f'+getMostRecentCall()[1:])
