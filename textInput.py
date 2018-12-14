import globals
# Class for creating text input boxes.
#
# Required params;
# x         - X coord of the box
# y         - Y coord of the box
# boxWidth  - Width of the box
# boxHeight - Height of the box

# Optional params;
# boxColor  - Color of the box, made using color(). Default is white.
# textColor - Color of the text, made using color(). Default is black.
# textSize  - Size of the text. Default is boxHeight*0.6
# command   - The function to execute after the user presses Enter/Return. Defaults to None.
# writable  - Whether to allow players to type in this box. Default is true.

class textBox:
    def __init__(self, x, y, boxWidth, boxHeight, **kwargs):
        #Required params
        self.x = x
        self.y = y
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        
        #Optional params
        self.boxColor = kwargs.get("boxColor", color(255, 255, 255, 255))
        self.textColor = kwargs.get("textColor", color(0, 0, 0, 0))
        self.textSize = kwargs.get("textSize", self.boxHeight*0.6)
        self.command = kwargs.get("command", None)
        self.numeric = kwargs.get("numeric", False)
        self.writable = kwargs.get("writable", True)
        
        self.text = ""
        self.activeTimer = millis()
        
    def draw(self):
        pushStyle()
        pushMatrix()
        rectMode(CORNER)
        textAlign(LEFT)
    
        textSize(self.textSize)

        translate(0, self.boxHeight, 0)
        fill(self.boxColor)
        rect(self.x, self.y, self.boxWidth, 0-self.boxHeight)
        
        if globals.activeTextBox == self:
            fill(self.textColor)
            line((self.x+10), (self.y-3), ((self.boxWidth+self.x)-10), (self.y-3))
        
        fill(self.textColor)
        text(self.text, (self.x+10), (self.y-self.boxHeight/5))
        
        popStyle()
        popMatrix()
        
    def input(self, inputKey, inputCode):
        inputKey = str(inputKey)
        if len(inputKey) == 1:
            if not inputKey == CODED:
                if inputKey == BACKSPACE:
                    self.text = self.text[:-1]
                    if inputCode == CONTROL:
                        while not self.text.endswith(' '):
                            self.text = self.text[:-1]
                elif inputKey == ENTER or inputKey == RETURN:
                    if self.command != None:
                        self.command(self.text)
                elif textWidth(self.text) < self.boxWidth+75:
                    self.text+=str(inputKey)
            
    def active(self):
        if self.writable:
            globals.activeTextBox = self
        
def check():
    baseX = globals.baseScaleXY.X
    baseY = globals.baseScaleXY.Y
    pool = [] + globals.textBoxDict["global"]
    if globals.currentMenu in globals.textBoxDict:
        pool+= globals.textBoxDict[globals.currentMenu]
        
    isInsideBox = False
    for textBox in pool:
        if (textBox.x*baseX <= mouseX <= (textBox.x+textBox.boxWidth)*baseX) and (textBox.y*baseY <= mouseY <= (textBox.y+textBox.boxHeight)*baseY):
            isInsideBox = True
            textBox.active()
    if not isInsideBox:
        globals.activeTextBox = None
