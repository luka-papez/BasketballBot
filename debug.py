import numpy as np
import cv2

def destroy_windows():
  # stupid OpenCV bug
  cv2.destroyAllWindows()
  for i in range(5):
    cv2.waitKey(1)

# TODO: python static variables?
window_count = 0
default_name = "Image"
def display_image(image, name = default_name):
  global window_count
  winname, window_count = (name + str(window_count), window_count + 1) if name == default_name else (name, window_count)

  cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
  cv2.resizeWindow(winname, 600, 600)
  cv2.imshow(winname, image)
  cv2.waitKey(2000)

def draw_trajectory(trajectory, img_dbg):
  for p in trajectory:
    cv2.circle(img_dbg, (p[0], p[1]), 5, (255, 0, 0), 2)

def draw_basket(basket_center, img_dbg):
  cv2.circle(img_dbg, (basket_center[0], basket_center[1]), 5, (0, 255, 0), 2)
  
def draw_ball(ball_center, img_dbg):
  cv2.circle(img_dbg, (ball_center[0], ball_center[1]), 5, (0, 0, 255), 2)



