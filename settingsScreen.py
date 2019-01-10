# coding= utf-8
import globals
import data
import prime_number_menu
from util import *
from Button import Button
from Object import Object

def init():
    global buttons, categories, onScreenText
    
    categories = dict()
    categoryPos = dict()
    
    r = RoundRect(-15, -15, 30, 30, 5)
    Object.startGroup()
    
    bgRadioButton1 = Button(0, 0, r.copy())
    bgRadioButton1.applyStyle('radio')
    bgRadioButton1.radioGroup = 'bg_select'
    bgRadioButton1.name = 'Blue'
    bgRadioButton1.value = 'background'
    bgRadioButton1.color_value = color(0,180, 250)
    bgRadioButton1.releaseAction = setBackground
    
    bgRadioButton2 = Button(0, 0, r.copy())
    bgRadioButton2.applyStyle('radio')
    bgRadioButton2.radioGroup = 'bg_select'
    bgRadioButton2.name = 'Orange'
    bgRadioButton2.value = 'background-1'
    bgRadioButton2.color_value = color(250, 140, 0)
    bgRadioButton2.releaseAction = setBackground
    
    bgRadioButton3 = Button(0, 0, r.copy())
    bgRadioButton3.applyStyle('radio')
    bgRadioButton3.radioGroup = 'bg_select'
    bgRadioButton3.name = 'Green'
    bgRadioButton3.value = 'background-2'
    bgRadioButton3.color_value = color(0, 200, 0)
    bgRadioButton3.releaseAction = setBackground
    
    bgRadioButton4 = Button(0, 0, r.copy())
    bgRadioButton4.applyStyle('radio')
    bgRadioButton4.radioGroup = 'bg_select'
    bgRadioButton4.name = 'Purple'
    bgRadioButton4.value = 'background-3'
    bgRadioButton4.color_value = color(200, 0, 250)
    bgRadioButton4.releaseAction = setBackground
    
    bgRadioButton5 = Button(0, 0, r.copy())
    bgRadioButton5.applyStyle('radio')
    bgRadioButton5.radioGroup = 'bg_select'
    bgRadioButton5.name = 'Gray'
    bgRadioButton5.value = 'background-4'
    bgRadioButton5.color_value = color(130)
    bgRadioButton5.releaseAction = setBackground
    
    categories['Background Select'] = Object.endGroup()
    categoryPos['Background Select'] = Vector2(width*0.55, 0)
    for o in categories['Background Select']:
        if o.name == globals.userConfig['settings']['bg_select']:
            o.releaseAction(o, -1)
            o.activated = True
    
    Object.startGroup()
    
    animCheckbox = Button(0, 0, r.copy())
    animCheckbox.applyStyle('checkbox')
    animCheckbox.name = 'Enable button animations'
    animCheckbox.releaseAction = toggleSettings
    animCheckbox.value = 'objectAnims_OnOff'
    animCheckbox.activated = globals.userConfig['settings']['objectAnims_OnOff']
    
    masterAnimCheckbox = Button(0, 0, r.copy())
    masterAnimCheckbox.applyStyle('checkbox')
    masterAnimCheckbox.name = 'Enable transitions'
    masterAnimCheckbox.releaseAction = toggleSettings
    masterAnimCheckbox.value = 'anims_OnOff'
    masterAnimCheckbox.activated = globals.userConfig['settings']['anims_OnOff']
    
    categories['Animations'] = Object.endGroup()
    categoryPos['Animations'] = Vector2(width*0.25, 0)
    
    Object.startGroup()
    
    fontSelectRadio1 = Button(0, 0, r.copy())
    fontSelectRadio1.applyStyle('radio')
    fontSelectRadio1.radioGroup = 'font_select'
    fontSelectRadio1.name = 'Sans Serif'
    fontSelectRadio1.fullName = 'SansSerif.plain'
    fontSelectRadio1.releaseAction = setFont
    
    fontSelectRadio2 = Button(0, 0, r.copy())
    fontSelectRadio2.applyStyle('radio')
    fontSelectRadio2.radioGroup = 'font_select'
    fontSelectRadio2.name = 'Open Sans'
    fontSelectRadio2.fullName = 'Open Sans'
    fontSelectRadio2.releaseAction = setFont
    
    fontSelectRadio3 = Button(0, 0, r.copy())
    fontSelectRadio3.applyStyle('radio')
    fontSelectRadio3.radioGroup = 'font_select'
    fontSelectRadio3.name = 'Lucida Sans'
    fontSelectRadio3.fullName = 'Lucida Sans Regular'
    fontSelectRadio3.releaseAction = setFont
    
    fontSelectRadio4 = Button(0, 0, r.copy())
    fontSelectRadio4.applyStyle('radio')
    fontSelectRadio4.radioGroup = 'font_select'
    fontSelectRadio4.name = 'Consolas'
    fontSelectRadio4.fullName = 'Consolas'
    fontSelectRadio4.releaseAction = setFont
    
    categories['Fonts'] = Object.endGroup()
    for o in categories['Fonts']:
        if not o.fullName in PFont.list():
            categories['Fonts'].remove(o)
            continue
        if o.name == globals.userConfig['settings']['font']:
            o.releaseAction(o, -1)
            o.activated = True
        else:
            o.activated = False
    
    Object.startGroup()

    backButton = Button(37, 37, RoundRect(-25, -25, 50, 50) * 0.75)
    backButton.releaseAction = gotoMainMenu
    backButton.textSize *= 3
    backButton.applyStyle('compact')
    backButton.description = 'Main menu'
    backButton.icon = globals.imgIndex['back'].copy()
    backButton.iconScale = 0.75
    backButton.iconColor = color(0,0)
    
    buttons = Object.endGroup()
    
    # I know the following chunk is messy code, but it works!
    # It helps cache a lot of the data used for custom graphics and aligning text and buttons.
    textSizeHeader = 25
    textSizeButtons = 20
    
    textSize(textSizeHeader)
    i = 15 + textAscent()/2
    offsetX = width*0.35
    sizeX = width*0.225
    for key, group in categories.items():
        pushStyle()
        textSize(textSizeHeader)
        
        if key in categoryPos:
            offsetX = categoryPos[key].X
            i = 15 + textAscent()/2 + categoryPos[key].Y
        
        i += textHeight(key) - textDescent()
        onScreenText.append((key, Vector2(offsetX - 15, i), textSizeHeader))
        i += textHeight(key)
        
        pg = createGraphics(int(sizeX), 2)
        pg.beginDraw()
        for val in range(int(sizeX)):
            c = lerpColor(color(0), color(0,0), float(val) / sizeX)
            pg.stroke(c)
            pg.line(val - 15, 0, val - 15, 1)
        pg.endDraw()
        onScreenFeatures.append((pg, Vector2(offsetX+sizeX/2-15, i)))
        
        i += 30
        for o in group:
            o.setPosition(offsetX, i)
            onScreenText.append((o.name, Vector2(offsetX + (o.shape.width + textAscent()*1.5)/2, i + (textAscent()-textDescent()) / 2), textSizeButtons))
            i += o.shape.height * 1.5
        popStyle()

onScreenText = list()
onScreenFeatures = list()
def draw():
    width = 1133
    height = 600
    scale(*globals.baseScaleXY)
    
    pushMatrix()
    fill(0)
    textSize(40)
    s = 'Settings'
    translate(0, textHeight(s)*2 + textDescent())
    text(s, width/2 - textWidth(s)/2, -textDescent())
    
    pushStyle()
    # Cache for fontsize so it is not called excessively
    _fontsize = 0
    for txt, pos, fontsize in onScreenText:
        if not _fontsize == fontsize:
            textSize(fontsize)
            _fontsize = fontsize
        text(txt, pos.X, pos.Y)
    popStyle()
    
    for pg, pos in onScreenFeatures:
        image(pg, pos.X, pos.Y)

    for group in categories.values():
        for o in group:
            o.update()
    popMatrix()
    
    for o in buttons:
        o.update()
    
def gotoMainMenu(*args):
    if args[1] == LEFT:
        globals.currentMenu = "mainMenu"

def setFont(self, *args):
    globals.userConfig['settings']['font'] = self.name
    data.saveData()
    globals.font = createFont(self.name, 100, True)
    textFont(globals.font)

def toggleSettings(self, *args):
    globals.userConfig['settings'][self.value] = self.activated
    data.saveData()

def setBackground(self, *args):
    globals.backgroundImgName = self.value
    globals.backgroundImg = globals.imgIndex[self.value].copy()
    globals.userConfig['settings']['bg_select'] = self.name
    globals.userConfig['settings']['primary_color'] = self.color_value
    data.saveData()
