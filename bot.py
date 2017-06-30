import cv2
import numpy as np

from screenshot import Screenshot
from vision import find_basket, find_ball
from shooting import patterns_overlap, determine_shot_location
from mouse import perform_mouse_drag, GameAreaShit, click_play_again
from time import sleep

""" General TODOs """
# TODO: basket is found as (x, y) instead of (y, x)
# TODO: logging
# TODO: learn how to write python documentation
# TODO: important comment should be in docstrings and not as comments

# TODO: better variable name
pattern_length = 10

# how much to sleep between two consecutive measurements
measurement_interval = 0.05
if __name__ == '__main__':
  # repeat until victory

  s = Screenshot()
  screen_and_crop = lambda: crop_game_area(s.screenshot())[0]
  shots_hit = 0
  # shooting loop
  while True:
    print 'Starting iter'
    
    trajectory = []
    first_pattern = []
    for _ in xrange(0, pattern_length):
      img_screen = screen_and_crop()

      measurement = find_basket(img_screen)
      first_pattern.append(measurement)
      trajectory.append(measurement)

      sleep(measurement_interval)

    # check if the basket moved at all, if not there's no need to learn the trajectory
    if len(first_pattern) == len(set(first_pattern)):
      current_pattern = []
      # measurement loop
      while not patterns_overlap(first_pattern, current_pattern):
        img_screen = screen_and_crop()

        if len(current_pattern) == pattern_length:
          current_pattern.pop(0)

        measurement = find_basket(img_screen)
        current_pattern.append(measurement)
        trajectory.append(measurement)
        
        sleep(measurement_interval)

    # TODO: should probably pop the last pattern from the trajectory as it overlaps
    trajectory = trajectory[0:-pattern_length]
         
    img_screen, shift = crop_game_area(s.screenshot())
    img_dbg = img_screen.copy()
    GameAreaShift.shift = shift
    # TODO: what if the ball moves?
    # find the ball coordinates
    ball_center = find_ball(img_screen, img_dbg)
    basket_current = find_basket(img_screen, img_dbg)

    # determine where to shoot based on the current basket location    
    mouse_start = ball_center
    mouse_end = determine_shot_location(trajectory, basket_current)
    
    # do the computed mouse movement, move the mouse in the ball, and then drag it to the basket
    perform_mouse_drag(mouse_start, mouse_end)
    
    # Wait for result
    sleep(3)
    if missed_shot(img_screen):
      print 'Hit %d shots in this game' % shots_hit
      shots_hit = 0
      click_play_again(img_screen)
    else:
      shots_hit = shots_hit + 1
    
    
    
