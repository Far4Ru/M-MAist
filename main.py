from PIL import ImageGrab, ImageOps
from numpy import *
import os
import time
import ctypes
import win32api, win32con
import requests
import keyboard

user32 = ctypes.windll.user32
screenSize = user32.GetSystemMetrics(0), user32.GetSystemMetrics(1)

def grab():
    box = ()
    im = ImageOps.grayscale(ImageGrab.grab())
    a = array(im.getcolors())
    a = a.sum()
 
def leftClick():
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
      time.sleep(.1)
      win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
      print("Click")
def leftDown():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(.1)
    print('Left Down')
         
def leftUp():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(.1)
    print('Left Up')
    
def mousePos(cord):
    win32api.SetCursorPos((cord[0], cord[1]))
    
def get_cords():
    x,y = win32api.GetCursorPos()
    #x = x - x_pad
    #y = y - y_pad
    print(x,y)
    return (x,y)

def screenGrabByCoords(x1,y1,x2,y2):
    box = (x1,y1,x2,y2)
    im = ImageGrab.grab(box)
    #im.save(os.getcwd() + '\\snap__' + str(int(time.time())) + '.png', 'PNG')
    return im
    
def screenGrabAll():
    im = ImageGrab.grab()
    return im

def saveImage(im):
    im.save(os.getcwd() + '\\snap__' + str(int(time.time())) + '.png', 'PNG')
    
def imageToGray(im):
    im = ImageOps.grayscale(im)
    return im

def getLeftBarByGray(value):
    im = imageToGray(screenGrabByCoords(0,0,screenSize[0],screenSize[1]))
    leftUp = (screenSize[0],screenSize[1])
    rightDown = (0,0)
    for i in range(screenSize[1]//6,5*screenSize[1]//6):
        for j in range(screenSize[0]-1,4*screenSize[0]//5,-1):
            if(im.getpixel((j,i)) > value):
                if(j < leftUp[0] and i < leftUp[1]):
                   leftUp = (j,i)
                if(j > rightDown[0] and i > rightDown[1]):
                    rightDown = (j,i)
    print(leftUp[0],leftUp[1],rightDown[0],rightDown[1])
    return [leftUp[0],leftUp[1],rightDown[0],rightDown[1]]
    #mousePos(leftUp)
    #im = screenGrabByCoords(leftUp[0],leftUp[1],rightDown[0],rightDown[1])
    #return im

def print_pressed_keys(e):
    print(e, e.event_type, e.name)

#keyboard.hook(print_pressed_keys)

def search_windows_border():
    mousePos((1356,861))
    im = screenGrabAll()
    c = 0
    max_coords = [[(0,0),(0,0)],[(0,0),(0,0)]]
    max_c = 0
    cur_start_coords = (0,0)
    for i in range(screenSize[1]):
        for j in range(screenSize[0]):
            pix_color = im.getpixel((j,i))
            if(pix_color[2] < 50 and pix_color[2] > 30):
                if(pix_color[1] < 35 and pix_color[1] > 15):
                    if(pix_color[0] < 30 and pix_color[0] > 5):
                        mousePos((j,i))
                        im.putpixel((j,i),(255,255,255))
                        if(c == 0):
                            cur_start_coords = (j,i)
                        c+=1
                    else:
                        if(c >= max_c):
                            max_c = c
                            max_coords.append([cur_start_coords,(j,i)])
                        c = 0
                else:
                    if(c >= max_c):
                        max_c = c
                        max_coords.append([cur_start_coords,(j,i)])
                    c = 0
            else:
                if(c >= max_c):
                    max_c = c
                    max_coords.append([cur_start_coords,(j,i)])
                c = 0
    top_pix = max_coords.pop()
    im.putpixel(top_pix[0],(255,255,255))
    im.putpixel(top_pix[1],(255,255,255))
    bot_pix = max_coords.pop()
    im.putpixel(bot_pix[0],(255,255,255))
    im.putpixel(bot_pix[1],(255,255,255))
    #saveImage(im)
    #im = screenGrabByCoords(max(top_pix[0][0],bot_pix[0][0]),min(top_pix[0][1],bot_pix[0][1]),min(top_pix[1][0],bot_pix[1][0]),max(top_pix[1][1],bot_pix[1][1]))
    saveImage(im)
    mousePos((1356,861))
    #2 линии, искать в разных локациях изменения цветов на линии
    #R: [95-215]
    #G: [70-170]
    #B: [20-120]



def get_color_current_pos_color():
    get_color_by_coords(get_cords())

def get_color_by_coords(coords):
    im = screenGrabAll()
    print(im.getpixel(coords))

def get_task_window():
    mousePos((1356,861))
    leftClick()
    print('World')

def grab_window():
   #getLeftBarByGray(240)
    get_task_window()
    #saveImage(im)
    
def main():
    
    keyboard.add_hotkey('Ctrl + 1', lambda: print('Hello')) #def control
    keyboard.add_hotkey('Ctrl + 2', grab_window) #main process, Task Windows
    keyboard.add_hotkey('Ctrl + 3', get_color_current_pos_color) #Pos Color
    keyboard.add_hotkey('Ctrl + 5', search_windows_border) #search + save image
    
    print('Ready')
    keyboard.wait('Ctrl + Q')
    

    #screenGrab()
    #get_cords()
    #mousePos((1280,265))
    #leftClick()
    #leftClick()
    #leftClick()
    #r = requests.Session()
    #r.auth = ('id','1')
    #r.post('.php',{'character':'LAZER','task':'Дозор', 'cell_value':1})
    
    #r.text
if __name__ == '__main__':
    main()
