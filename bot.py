# TODO: these are probably no longer needed
import cv2
import numpy as np

from time import sleep

from screenshot import Screenshot
from vision import find_basket, find_ball, find_game_area_shift, crop_game_area, missed_shot
from control import patterns_overlap, determine_next_basket_position
from mouse import shoot, click_play_again
from debug import draw_trajectory, draw_ball, draw_basket, display_image

""" General TODOs """
# TODO: basket is found as (x, y) instead of (y, x)
# TODO: logging
# TODO: learn how to write python documentation
# TODO: important comment should be in docstrings and not as comments
# TODO: consistent use of ints for data storage

# how much to sleep between two consecutive measurements
if __name__ == '__main__':

  s = Screenshot()
  screen_and_crop = lambda: crop_game_area(s.screenshot())
  shots_hit = 0  
  pattern_length = 10
  measurement_interval = 0
  
  # shooting loop
  while True:
    
    trajectory = []
    
    # record the beggining of the pattern
    first_pattern = []
    for _ in xrange(0, pattern_length):
      img_screen = screen_and_crop()

      measurement = find_basket(img_screen)
      first_pattern.append(measurement)
      trajectory.append(measurement)

      sleep(measurement_interval)

    # check if the basket moved at all, if not there's no need to learn the trajectory
    # TODO: this is completely broken
    if len(first_pattern) == len(set(tuple(map(tuple, first_pattern)))):
    # TODO: stricter condition could be if len(set(first_pattern)) != 1 or something but could fail sometimes
      print 'Learning pattern.'
      current_pattern = []
      # measurement loop
      while not patterns_overlap(first_pattern, current_pattern):
        img_screen = screen_and_crop()

        # remove the first measurement from current pattern
        if len(current_pattern) == pattern_length:
          current_pattern.pop(0)

        measurement = find_basket(img_screen)
        current_pattern.append(measurement)
        trajectory.append(measurement)
        
        sleep(measurement_interval)

    # pop the last pattern from the trajectory as it starts to overlap
    trajectory = trajectory[0 : -pattern_length]
         
    # find the shift of the game area  
    img_screen = s.screenshot()
    shift = find_game_area_shift(img_screen)

    img_screen = crop_game_area(img_screen)
    # TODO: what if the ball moves?
    # find the ball coordinates
    ball_center = find_ball(img_screen)
    basket_current = find_basket(img_screen)
    
    # TODO: remove debugging
    img_dbg = img_screen.copy()

    # determine where to shoot based on the current basket location    
    basket_next = determine_next_basket_position(trajectory, basket_current)
    
    # do the shooting mouse movement
    shoot(shift, ball_center, basket_next)
    
    # Wait for result
    sleep(2)
    draw_trajectory(trajectory, img_dbg)
    draw_ball(ball_center, img_dbg)
    draw_basket(basket_current, img_dbg)
    #display_image(img_dbg)
    cv2.imwrite('shot' + str(shots_hit) + '.png', img_dbg)

    print trajectory

    img_screen = screen_and_crop()
    if missed_shot(img_screen):
      print 'Hit %d shots in this game' % shots_hit
      shots_hit = 0
      click_play_again(shift, img_screen)
    else:
      shots_hit = shots_hit + 1
    
    
    
