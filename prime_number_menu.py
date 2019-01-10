import globals
from util import *

last_prime = -1

menu_width = 200
menu_height = 200
menu_fontsize = 25
menu_fontcolor = color(0)
menu_columns = 4
menu_rows = 5

menu_header_height = 30
menu_header_fontsize = 20
menu_header_bgcolor = color(255)
menu_header_fontcolor = color(0)

menu_corner_radius = 15

menu_drag_pos = None
menu_offset = Vector2(0,0)

def draw(mousePressed=False):
    global last_prime
    
    global menu_width
    global menu_height
    global menu_fontsize
    global menu_fontcolor
    global menu_columns
    global menu_rows
    
    global menu_header_height
    global menu_header_fontsize
    global menu_header_bgcolor
    global menu_header_fontcolor
    
    global menu_corner_radius
    global menu_drag_pos
    global menu_offset
    
    pushStyle()
    pushMatrix()
    pushMatrix()
    g.setMatrix(getCurrentInvMatrix())
    mousePos = Vector2(mouseX, mouseY).getModelPos()
    shape = Rectangle(-getWidth()/2 - menu_offset.X, -getHeight()/2 - menu_offset.Y, getWidth(), getHeight())
    if mousePressed and (shape.contains(*mousePos) or not menu_drag_pos == None):
        if menu_drag_pos == None:
            menu_drag_pos = Vector2(mouseX, mouseY).getModelPos()
        menu_offset += menu_drag_pos - Vector2(mouseX, mouseY).getModelPos()
        menu_drag_pos = Vector2(mouseX, mouseY).getModelPos()
    else:
        menu_drag_pos = None
    popMatrix()
    translate(*-menu_offset)
    translate(-getWidth()/2, -getHeight()/2)
    
    rectMode(CORNER)
    strokeWeight(1)
    
    menu_header_bgcolor = globals.userConfig['settings']['primary_color']
    transitionFill('prime_number_menu.py#header_bgcolor', 250, menu_header_bgcolor)
    translate(0, menu_header_height)
    rect(0, -menu_header_height, menu_width, menu_header_height, menu_corner_radius, menu_corner_radius, 0, 0)
    fill(255)
    rect(0, 0, menu_width, menu_height, 0, 0, menu_corner_radius, menu_corner_radius)
    fill(0)
    
    textAlign(CENTER)
    
    textSize(menu_fontsize)
    fill(menu_fontcolor)
    coord = [0, 0]
    column_width = menu_width / float(menu_columns)
    row_height = menu_height / float(menu_rows)
    # Yeah i didn't bother caching the list
    # I know, minor change, but it didn't impact performance much so i didn't really care
    for i in get_prime_numbers(menu_rows*menu_columns):
        while textAscent() + textDescent() > row_height:
            menu_fontsize -= 1
            textSize(menu_fontsize)
        while textWidth(str(i)) > column_width:
            menu_fontsize -= 1
            textSize(menu_fontsize)
            
        text(str(i), column_width * (coord[0]+0.5), row_height * (coord[1]+0.5) + textHeight()/2)
        last_prime = i
        coord[0] += 1
        if coord[0] == menu_columns:
            coord[0] = 0
            coord[1] += 1
            if coord[1] == menu_rows:
                break
    
    textSize(menu_header_fontsize)
    header_txt = 'Prime numbers 2-'+(str(last_prime) if not last_prime == -1 else 'N/A')
    while textAscent() + textDescent() > menu_header_height:
        menu_header_fontsize -= 1
        textSize(menu_header_fontsize)
    while textWidth(header_txt) > menu_width:
        menu_header_fontsize -= 1
        textSize(menu_header_fontsize)
    text(header_txt, menu_width/2, -menu_header_height/2 + textHeight()/2)
    
    popMatrix()
    popStyle()

def getHeight():
    global menu_height
    global menu_header_height
    return menu_height + menu_header_height

def getWidth():
    global menu_width
    return menu_width

def get_prime_numbers(lmit=20):
    primes = []
    n = 2
    # Wait until the desired amount of primes are found
    while len(primes) < lmit:
        not_divisible = True
        # Loop through numbers from 2 -> n-1
        for x in range(2, n):
            # Check if n is divisible by x, where x: 1 < x < n
            if (n / float(x)) % 1 == 0:
                not_divisible = False
                break
        if not_divisible:
            # Add the prime number to the list
            primes.append(n)
        n += 1
    return primes
