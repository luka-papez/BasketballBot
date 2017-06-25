import cv2
import numpy as np
from functions import screengrab, find_basket, find_ball, perform_mouse_drag
from time import sleep

# TODO: basket could probably found more robustly with template matching as it doesn't rotate
# TODO: basket is found as (x, y) instead of (y, x)
# TODO: zero out everything except game area, clean up the code

from pymouse import PyMouse

s = screengrab()
if __name__ == '__main__':
  # repeat until victory

  while True:
    print 'Starting iter'
    # get screenshot
    img_screen = None 
    while img_screen is None:
      img_screen = s.screen()
      
    img_dbg = img_screen
    print 'Grabbed screen'
    
    # localize the basket coordinates using template matching
    sleep(2) # TODO sleeping because poor basket localization performance when net is moving
    basket_center = find_basket(img_screen, img_dbg)
    print 'Found basket'
    
    m = PyMouse()
  
    m.move(basket_center[0], basket_center[1])
    
    # TODO: this is really ugly
    # zero out unimportant areas for finding the ball
    # above the basket
    img_screen[0 : basket_center[1], :, : ] = 0
    # around the basket
    img_screen[:, 0 : (basket_center[0] - 200), :] = 0
    img_screen[:, (basket_center[0] + 200) : -1, :] = 0
    # bottom of the screen
    img_screen[-70:-1, :, :] = 0
    
    # find the ball coordinates using Hough circle transform
    ball_center = find_ball(img_screen, img_dbg)
    print 'Found ball'
    
    #cv2.imshow('aaa', img_dbg)
    #cv2.waitKey(0)
    
    # compute the required movement
    # TODO: what if the basket is moving?
    mouse_start = ball_center
    mouse_end = basket_center
    
    # do the computed mouse movement, move the mouse in the ball, and then drag it to the basket
    perform_mouse_drag(mouse_start, mouse_end)
    
    print 'Did movement'
    
    
    
