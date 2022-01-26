# file: badapple.py
# description: generate and display txt in cmd.exe
# translated from Touhou - Bad Apple mp4 clip
# author: Hiukong Dan
# version: 1.0    5/May/2021

"""
TODO:
improve resolution of the translated ascii code image
manipulate cmd buffer directly and using another method instead of print
hide cursor if possible (the last line always showing blank due to appearance of cursor)
generating txt: using a compress algorithm to store converted strings
"""

import cv2
import numpy as np
import playsound

import math
import os
import time
import threading
import win32console, win32gui
from win32console import *


from configparser import ConfigParser
from ctypes import wintypes

from compressTxt import decompress

STD_INPUT_HANDLE  = wintypes.DWORD(-10).value
STD_OUTPUT_HANDLE = wintypes.DWORD(-11).value
STD_ERROR_HANDLE  = wintypes.DWORD(-12).value

def getNextFrameTxt(frame):
    """
    used by function preprocess
    translate each frame from original frame
    to a much low resolution frame (specifically current cmd column/row numbers)
    using character '#' for white pixel,
    using character ' ' for black pixel,
    """
    tmp = frame.reshape(1, frame.shape[0] * frame.shape[1] * len(frame[0][0]))
    
    tmp = [round(tmp[0][x]/255) for x in range(0, len(tmp[0]), 3)]
    
    # transform badapple pixels to single values, 0 for black, 1 for white
    raw_pixels = np.array(tmp).reshape(frame.shape[0], frame.shape[1])
    
    # print(raw_pixels)
    
    cv2.imshow('frame', frame)
    
    win_size = os.get_terminal_size()
        
    ret = []
    for row_count in range(0, len(raw_pixels), int(raw_pixels.shape[0]/win_size[1])):
        row = raw_pixels[row_count]
        ret.append(["#" if row[x] == 0 else " " for x in range(0, raw_pixels.shape[1], int(raw_pixels.shape[1]/win_size[0]))])
        
    # print("converted shape: %d, %d" % (len(ret), len(ret[0])))
    
    res = ""
    for row in ret:
        res += ''.join(row)
        res += "\n"
        
    return res
    
    
        
def preprocess():
    """
    used to generated bad apple txt from original mp4 data
    """
    win_size = os.get_terminal_size()
    config_file = "config.ini"
    config = ConfigParser()
    config["SCREEN_SIZE"] = {
                            columns : win_size[0],
                            rows : win_size[1]
                            }
    with open(config_file, 'w') as conf_file:
        conf_file.write(config)
        
        
    with open("badapple.txt", 'w') as fil:
        cap = cv2.VideoCapture("Touhou - Bad Apple.mp4")
        while(cap.isOpened()):
            ret, frame = cap.read()
            if(ret == True):
                fil.write(getNextFrameTxt(frame))
        cap.release()
        cv2.destroyAllWindows()
        fil.writelines((" "*win_size[0]+"\n") * win_size[1])
        
        
        
        
def setup_cmd_buffer():
    config = ConfigParser()
    config.read("config.ini")
    win_size = (config["SCREEN_SIZE"]["columns"], config["SCREEN_SIZE"]["rows"])
    win_size = (int(win_size[0]), int(win_size[1]))

    console_buffer_old = win32console.GetStdHandle(STD_OUTPUT_HANDLE)
    """
    win_handle = win32console.GetConsoleWindow()
    place_info = win32gui.GetWindowPlacement(win_handle)
    win32gui.SetWindowPos(win_handle, 0, place_info[-1][0], place_info[-1][1],
        100, 100, place_info[0])
    """
    console_buffer_new = win32console.CreateConsoleScreenBuffer()
    console_buffer_new.SetConsoleCursorInfo(5, False);
    console_window_buffer_info = console_buffer_old.GetConsoleScreenBufferInfo()
    new_win_size = console_window_buffer_info['Size']
    win_rect = console_window_buffer_info['Window']
    new_win_size.X = win_rect.Right - win_rect.Left + 1
    new_win_size.Y = win_rect.Bottom - win_rect.Top + 1
    
    for key in console_window_buffer_info:
        print("{}: {}".format(key, console_window_buffer_info[key]))
    
    if new_win_size.X < win_size[0]: new_win_size.X = win_size[0]
    if new_win_size.Y < win_size[1]: new_win_size.Y = win_size[1]
    
    win_rect.Right = win_rect.Left + new_win_size.X - 1
    win_rect.Bottom = win_rect.Top + new_win_size.Y - 1
    
    print(win_rect)

    new_win_size.Y = 999
    console_buffer_new.SetConsoleScreenBufferSize(new_win_size)
    console_buffer_new.SetConsoleWindowInfo(True, win_rect)
    console_buffer_new.SetConsoleActiveScreenBuffer()
    win32console.SetConsoleTitle("B A D A P P L E")
        
    return console_buffer_new
        
        
        
        
def processBadAppleTxt():
    """
    process string data generated by function preprocess
    and display frame by frame using a lag calculated method
    """
    win_size = os.get_terminal_size()
    frame_rate = 30
    current_frame = 0
    start_time = time.time()
    
    console_buffer_new = setup_cmd_buffer()
    
    with open("compressed_badapple.txt", 'r') as fil:
        while True:
            try:
                display = ""
                for x in range(win_size[1]-1):
                    display = decompress(fil.readline())
                    display = display[:-2]
                    console_buffer_new.WriteConsoleOutputCharacter(display, win32console.PyCOORDType(X=0, Y=x))
                fil.readline()
                #print(display)
                next_frame_time = (current_frame + 1) * 1 / frame_rate + start_time
                current_frame += 1
                lag = next_frame_time - time.time()
                if lag > 0:
                    time.sleep(lag)
            except AssertionError as error:
                print(error)
                break
    

    

def playBadAppleSound():
    """
    play audio using playsound
    """
    playsound.playsound("Touhou - Bad Apple.mp3")

if __name__ == "__main__":
    # process for your cmd window
    # preprocess()
    display_task = threading.Thread(target=processBadAppleTxt)
    playsound_task = threading.Thread(target=playBadAppleSound)
    
    display_task.start()
    playsound_task.start()
    
    
    
    """
    # opencv test code
    cap = cv2.VideoCapture("Touhou - Bad Apple.mp4")
    while(cap.isOpened()):
        ret, frame = cap.read()
        if(ret == True):
            printNextFrame(frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
    
        else:
            break
    cap.release()
    cv2.destroyAllWindows()
    """
    
