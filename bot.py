import cv2
import numpy as np
from functions import Screengrab, find_basket, find_ball, perform_mouse_drag
from time import sleep

# TODO: basket could probably found more robustly with template matching as it doesn't rotate
# TODO: basket is found as (x, y) instead of (y, x)
# TODO: zero out everything except game area, clean up the code

from pymouse import PyMouse

s = Screengrab()
if __name__ == '__main__':
  # repeat until victory

  i = 1
  while True:
    print 'Starting iter'
    
    # get screenshot
    img_screen = s.screen()
    img_dbg = img_screen
    print 'Grabbed screen'
    #cv2.imwrite(str(i) + '.jpg', img_screen)
    
    # localize the basket coordinates using template matching
    basket_center1 = find_basket(img_screen, img_dbg)
    print 'Found basket at', basket_center1
    
    sleep(0.05)
    basket_center2 = find_basket(img_screen, img_dbg)
    print 'Found basket at', basket_center2
    
    # TODO: prediction of basket center could be more advanced than this
    # TODO: maybe obtain the basket coordinates for 10 second and then find the pattern and the right position?
    alpha = 1.25
    basket_center = basket_center1 + alpha * (basket_center2 - basket_center1)
    
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
    
    mouse_start = ball_center
    mouse_end = basket_center
    
    # do the computed mouse movement, move the mouse in the ball, and then drag it to the basket
    if mouse_start is not None and mouse_end is not None:
      perform_mouse_drag(mouse_start, mouse_end)
    
#    cv2.imshow('aaa', img_dbg)
    
    i = i + 1
    sleep(5)
    print 'Did movement'
    
    
    
