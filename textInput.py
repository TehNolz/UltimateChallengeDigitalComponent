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

class textBox:
    def __init__(self, x, y, boxWidth, boxHeight, **kwargs):
        #Required params
        self.x = x
        self.y = y
        self.boxWidth = boxWidth
        self.boxHeight = boxHeight
        
        #Optional params
        self.boxColor = kwargs.get("boxColor", color(255, 255, 255, 0))
        self.textColor = kwargs.get("textColor", color(0, 0, 0, 0))
        self.textSize = kwargs.get("textSize", self.boxHeight*0.6)
        self.command = kwargs.get("command", None)
        self.textLimit = kwargs.get("textLimit", 99999999)
        print(self.textLimit)
        
        self.text = ""
        self.activeTimer = millis()
        
    def draw(self):
        pushStyle()
        pushMatrix()
        rectMode(CORNER)
        textAlign(LEFT)
        
        translate(0, self.boxHeight, 0)
        fill(self.boxColor)
        rect(self.x, self.y, self.boxWidth, 0-self.boxHeight)
        
        if globals.activeTextBox == self:
            line(self.x+10, self.y-3, (self.boxWidth+self.x)-10, self.y-3)
        
        textSize(self.textSize)
        fill(self.textColor)
        text(self.text, self.x+10, self.y-self.boxHeight/5)
        
        popStyle()
        popMatrix()
        
    def input(self, inputkey):
        print(textWidth(self.text))
        print(self.boxWidth)
        
        if inputkey == BACKSPACE:
            self.text = self.text[:-1]
        elif (inputkey == ENTER or inputkey == RETURN) and (self.command != None):
            self.command(self, self.text)
        elif textWidth(self.text) < self.boxWidth+75:
            self.text+=str(inputkey)
            
    def active(self):
        globals.activeTextBox = self
