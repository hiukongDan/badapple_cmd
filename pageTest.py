import os
import time
from os import system


if __name__ == "__main__":
    win_size = os.get_terminal_size()
    
    white_page = " " * (win_size[0] * win_size[1])
    black_page = "#" * (win_size[0] * win_size[1])
    
    frame_rate = 30
    
    #seconds
    duration = 5
    
    isWhite = True
    
    
    while duration > 0:
        if isWhite:
            print(white_page)
        else:
            print(black_page)
            
        isWhite = not isWhite  
        
        # one frame
        duration -= 1/frame_rate
        time.sleep(1/frame_rate)
    
    
    system("mode con: cols=480 lines=360")
    