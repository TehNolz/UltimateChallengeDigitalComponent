import globals
import java.awt.Toolkit as Toolkit
import java.awt.datatransfer.Clipboard as Clipboard
import java.awt.datatransfer.DataFlavor as DataFlavor
import java.awt.datatransfer.StringSelection as StringSelection
from util import *
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
    allTextBoxes = list()
    def __init__(self, x, y, boxWidth, boxHeight, **kwargs):
        textBox.allTextBoxes.append(self)
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
        
        self.text = ['', '', ''] # this is a list of strings: text before the cursor, selected text, text after the cursor
        self.lastUpdate = millis()
        self.selected = False
        self.cursorTimeOffset = 0
        
        self.cursor = 0 #position of the cursor
        self.oldCursor = 0
        self.selectCursor = 0 #position of the second selector cursor
        self.clicked = False
        self.doubleClickDelay = 500
        self.lastClickMillis = 0
        self.doubleClick = False
        self.ignoreMousePos = False
        
        self.textAlignment = LEFT
        self.textHeight = 0

        self.placeholder = ''
        self.lastMousePos = Vector2(0,0)
    
    def draw(self, mousePressed=False):
        textSize(30)
        self.lastUpdate = millis()
        self.update_textSegments()
        pushStyle()
        pushMatrix()
        rectMode(CORNER)
        textAlign(self.textAlignment)
    
        textSize(self.textSize)

        translate(self.x, self.y, 0)
        
        pushMatrix()
        g.setMatrix(getCurrentInvMatrix())
        mousePos = Vector2(mouseX, mouseY).getModelPos()
        popMatrix()
        r = Rectangle(0, 0, self.boxWidth, self.boxHeight)
        if mousePressed and (r.contains(*mousePos) or self.clicked): # This figures out where in the string you clicked
            if not self.ignoreMousePos:
                Width = 10
                fullString = self.text[0] + self.text[1] + self.text[2]
                counter = 0
                movedCursor = False
                for c in fullString:
                    Width += textWidth(c)
                    counter+=1
                    if Width > mousePos.X:
                        Width -= textWidth(c)/2
                        if Width > mousePos.X:
                            self.cursor = counter-1
                        else:
                            self.cursor = counter
                        movedCursor = True
                        break
                if not movedCursor:
                    if Width < mousePos.X:
                        self.cursor = len(self.text[0] + self.text[1] + self.text[2])
                    else:
                        self.cursor = 0
            if not self.clicked:
                self.clicked = True
                self.selectCursor = self.cursor
                if millis() - self.lastClickMillis < self.doubleClickDelay and self.lastClickPos == mousePos:
                    if self.doubleClick:
                        self.ignoreMousePos = True
                        self.cursor = len(self.getFullText())
                        self.selectCursor = 0
                    else:
                        self.ignoreMousePos = True
                        self.doubleClick = True
                        
                        # Append a space because cursors should be able to be placed at len(str)+1
                        txt = self.getFullText() + ' '
                        
                        cursorStop = False
                        scursorStop = False
                        if isWordDelimiter(txt[self.cursor-1]): # This will only select matching characters
                            starterChar = txt[self.cursor-1]
                            while True:
                                if self.cursor < len(txt)-1 and txt[self.cursor] == starterChar:
                                    self.cursor += 1
                                else:
                                    cursorStop = True
                                    
                                if self.selectCursor > 0 and txt[self.selectCursor-1] == starterChar:
                                    self.selectCursor -= 1
                                else:
                                    scursorStop = True
                                
                                if cursorStop and scursorStop:
                                    break
                        else:
                            while True: # This scans words untill a stop delimiter or an end of the string is reached.
                                if self.cursor < len(txt)-1 and not isWordDelimiter(txt[self.cursor]):
                                    self.cursor += 1
                                else:
                                    cursorStop = True
                                    
                                if self.selectCursor > 0 and not isWordDelimiter(txt[self.selectCursor-1]):
                                    self.selectCursor -= 1
                                else:
                                    scursorStop = True
                                
                                if cursorStop and scursorStop:
                                    break
                self.lastClickPos = mousePos
                self.lastClickMillis = millis()
            self.update_textSegments()
        elif not mousePressed:
            self.clicked = False
            if millis() - self.lastClickMillis > self.doubleClickDelay:
                self.doubleClick = False
                self.tripleClick = False
            self.ignoreMousePos = False
            
        fill(self.boxColor)
        rect(0, 0, self.boxWidth, self.boxHeight)
        
        if self.cursor != self.oldCursor:
            self.cursorTimeOffset = millis()
            self.oldCursor = self.cursor
        self.textHeight = (self.boxHeight + textAscent() - textDescent())/2
        if globals.activeTextBox == self:
            if self.selected == False:
                self.selected = True
                self.cursorTimeOffset = millis()
                self.selectCursor = self.cursor
                
            if not len(self.text[1]) == 0:
                pushStyle()
                noStroke()
                fill(setAlpha(globals.userConfig['settings']['primary_color'], 200))
                rect(10 + textWidth(self.text[0]),
                     self.textHeight - textAscent(),
                     textWidth(self.text[1]),
                     textAscent() + textDescent())
                popStyle()
                
            stroke(self.textColor)
            if (millis() - self.cursorTimeOffset) % 1000 < 500:
                cursorPos = 10 + textWidth(self.getFullText()[:self.cursor])
                line(cursorPos,
                     self.textHeight + textDescent(),
                     cursorPos,
                     self.textHeight - textAscent())
        else:
            self.selected = False
        
        fill(self.textColor)
        txt = self.getFullText()
        if len(txt) == 0:
            txt = self.placeholder
            fill(lerpColor(self.textColor, color(255, 255, 255), 0.5))
        if self.textAlignment == CENTER:
            text(txt, self.boxWidth/2, self.textHeight)
        else:
            text(txt, 10, self.textHeight)
        
        popStyle()
        popMatrix()
        
    def input(self, key, keyCode):
        textSize(30)
        # key and keyCode are actually sets because i wanted multi key input, unlike a certain somebody
        
        if RIGHT in keyCode:
            while True: # This is basically a do while loop
                if not SHIFT in keyCode:
                    if self.cursor != self.selectCursor:
                        self.cursor = len(self.text[0]+self.text[1])
                    else:
                        self.cursor += 1
                    self.selectCursor = self.cursor
                else:
                    self.cursor += 1
                self.update_textSegments()
                if (not CONTROL in keyCode
                    or len(self.getFullText()) <= self.cursor
                    or self.getFullText()[self.cursor] in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?'):
                    break
        if LEFT in keyCode:
            while True:
                if not SHIFT in keyCode:
                    if self.cursor != self.selectCursor:
                        self.cursor = len(self.text[0])
                    else:
                        self.cursor -= 1
                    self.selectCursor = self.cursor
                else:
                    self.cursor -= 1
                self.update_textSegments()
                if (not CONTROL in keyCode
                    or self.cursor <= 0
                    or self.getFullText()[self.cursor-1] in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?'):
                    break
        
        if TAB in key:
            # This is the epidemic of lazy coding lol
            shiftedFocus = False
            currentScreenBoxes = list((_ for _ in textBox.allTextBoxes if millis() - _.lastUpdate < float(1000)/frameRate + 10 and _.writable))
            for tb in currentScreenBoxes:
                #i use a loop because i was retarded, and it works so shut up
                if currentScreenBoxes.index(self) - currentScreenBoxes.index(tb) == (1 if SHIFT in keyCode else -1):
                    globals.activeTextBox = tb
                    tb.cursor = self.cursor
                    tb.selectCursor = self.cursor
                    shiftedFocus = True
                    break
            if not shiftedFocus and not len(currentScreenBoxes) == 0:
                tb = (currentScreenBoxes[-1] if SHIFT in keyCode else currentScreenBoxes[0])
                globals.activeTextBox = tb
                tb.cursor = self.cursor
                tb.selectCursor = self.cursor
        
        if BACKSPACE in key:
            if len(self.text[1]) == 0:
                self.text[0] = self.text[0][:-1]
                self.cursor -= 1
                self.selectCursor -= 1
                if CONTROL in keyCode:
                    if not len(self.text[0]) == 0 and isWordDelimiter(self.text[0][-1]):
                        startingChar = self.text[0][-1]
                        while self.text[0][-1] == startingChar:
                            self.text[0] = self.text[0][:-1]
                            self.cursor -= 1
                            self.selectCursor -= 1
                    else:
                        while not len(self.text[0]) == 0 and not self.text[0][-1] in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?':
                            self.text[0] = self.text[0][:-1]
                            self.cursor -= 1
                            self.selectCursor -= 1
            elif self.cursor > self.selectCursor:
                self.cursor = self.selectCursor
            self.text[1] = ''
            self.selectCursor = self.cursor
            
        if DELETE in key:
            if len(self.text[1]) == 0:
                self.text[2] = self.text[2][1:]
                if CONTROL in keyCode:
                    while not len(self.text[2]) == 0 and not self.text[2][0] in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?':
                        self.text[2] = self.text[2][1:]
            elif self.cursor > self.selectCursor:
                self.cursor = self.selectCursor
            self.text[1] = ''
            self.selectCursor = self.cursor

        if ENTER in key or RETURN in key:
            if not self.command == None:
                self.command(self.text[0])
        
        if u'\x01' in key: # this is ctrl+a
            self.selectCursor = 0
            self.cursor = len(self.text[0] + self.text[1] + self.text[2])
        
        if u'\x18' in key: # this is ctrl+x
            tk = Toolkit.getDefaultToolkit()
            clipboard = tk.getSystemClipboard()
            sts = StringSelection(self.text[1])
            clipboard.setContents(sts, None)
            self.text[1] = ''
            self.cursor = len(self.text[0])
            self.selectCursor = self.cursor
            
        if u'\x03' in key: # this is ctrl+c
            tk = Toolkit.getDefaultToolkit()
            clipboard = tk.getSystemClipboard()
            sts = StringSelection(self.text[1])
            clipboard.setContents(sts, None)
            
        try:
            if u'\x16' in key: # this is ctrl+v
                #java lol
                self.text[1] = ''
                self.selectCursor = self.cursor
                tk = Toolkit.getDefaultToolkit()
                clipboard = tk.getSystemClipboard()
                self.text[0] += str(clipboard.getData(DataFlavor.stringFlavor))
                self.cursor = len(self.text[0])
                self.selectCursor = self.cursor
        except:
            log = globals.log
            log.error('Caught exception \'UnicodeEncodeError\'.')
            log.error('The encoding of the copied string is not supported.')
        
        if not CODED in key:
            for k in key:
                if k.isalnum() or k in ' ./\()"\'-:,.;<>~!@#$%^&*|+=[]{}`~?':
                    self.text[0] += str(k)
                    self.cursor = len(self.text[0])
                    self.selectCursor = self.cursor
                    self.text[1] = ''

        self.update_textSegments()
        while textWidth(self.getFullText()) > self.boxWidth - 20:
            self.text[0] = self.text[0][:-1]
            self.cursor -= 1
            self.selectCursor -= 1
        self.update_textSegments()
        
        #fuck this code
        '''
        inputKey = str(inputKey)
        if len(inputKey) == 1:
            if not self.numeric or inputKey in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]: #Probably a really shitty solution but w/e
                if inputKey == BACKSPACE:
                    self.text = self.text[:-1]
                    if inputCode == CONTROL:
                        while not self.text.endswith(' '):
                            self.text = self.text[:-1]
                elif inputKey == ENTER or inputKey == RETURN:
                    if self.command != None:
                        self.command(self.text)
                elif textWidth(self.text) < self.boxWidth+300:
                    self.text+=str(inputKey)
        '''
    
    def getFullText(self):
        return self.text[0] + self.text[1] + self.text[2]
    
    def update_textSegments(self):
        txt = self.text[0] + self.text[1] + self.text[2]
        self.cursor = constrain(self.cursor, 0, len(txt))
        self.selectCursor = constrain(self.selectCursor, 0, len(txt))
        if self.cursor > self.selectCursor:
            self.text = [txt[:self.selectCursor], txt[self.selectCursor:self.cursor], txt[self.cursor:]]
        else:
            self.text = [txt[:self.cursor], txt[self.cursor:self.selectCursor], txt[self.selectCursor:]]
    
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
