import cv2
import numpy as np

""" Local TODOs """
# TODO: duration of imports when imported locally? (eg. in function)
  
def find_game_area_shift(img_screen):
  # TODO: find the biggest rectangle after edge detection?
  # TODO: invent Hough rectangle transform to find the rectangle with specified aspect ratio?
  return np.int32((0, 0))

def missed_shot(img_screen):
  """
    Returns True if it's determined that the shot was missed (e.g. there is a play again button on screen)
  """
  # TODO: template match to the button
  return False

def crop_game_area(img_screen):
  """ 
    Crops the screenshot to leave only the game area.
    
    @param img_screen
    @return cropped_img_screen
  """
  # TODO: this function is far from finished, should use find_game_area_shift
  return img_screen

# TODO: remove img_dbg
def find_ball(img_screen, img_dbg = None):
  """
    Finds the ball center coordinates using Hough circle transform.
    Biggest circle found on screen is said to be the ball.
    Uses a lot of code from: 
      http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html

    @param img_screen image of the screen
    @param img_dbg image on which to draw the found circles, useful when debugging
    @return ball_center center of the ball as [y, x]
  """
  img_screen_bin = cv2.cvtColor(img_screen, cv2.COLOR_RGB2GRAY)
  # TODO: performing edge detection could remove a lot of unnecessary information and make circle detection more robust
  
  # TODO: tweak parameters to be more robust
  circles = cv2.HoughCircles(img_screen_bin, cv2.HOUGH_GRADIENT, 2, 500, minRadius = 20, maxRadius = 200)
  if circles is None:
    print "Couldn't find circles"
    return None
    
  # TODO: use int32?
  circles = np.uint16(np.around(circles))
  # TODO: no idea why OpenCV returns the results in this useless format, but this must be done
  circles = circles[0] 
  
  # if many circles are found, sort descending according to circle radius and use the biggest one
  if len(circles) > 1:
    print "Found many circles, this shouldn't happen. Using the biggest one."
    # TODO: ugly
    circles = list(circles)
    circles.sort(key=lambda circle: circle[2])
    circles = np.int32(circles)

  # TODO: this function should return the coordinates as (y, x) instead of (x, y)
  return circles[0][:-1]

# TODO: this could maybe be a static variable in find_basket? (if that exits in python)
img_basket = cv2.imread('basket.png')
def find_basket(img_screen, img_dbg = None):
  """
    Finds the center of the basket using template matching to predefined image
    http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
    @param img_screen image of the screen
    @param img_dbg image on which to draw the found circles, useful when debugging
    @return basket_center center of the basket as [y, x]
  """
  method = cv2.TM_CCOEFF_NORMED
  res = cv2.matchTemplate(img_screen, img_basket, method)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

  h, w, _ = img_basket.shape
  top_left = np.array(max_loc)
  bottom_right = np.array((top_left[0] + w, top_left[1] + h))

  if img_dbg is not None:
    cv2.rectangle(img_dbg, tuple(top_left), tuple(bottom_right), 255, 2)
  
  # TODO: this function should return the coordinates as (y, x) instead of (x, y)
  return (top_left + bottom_right) / 2


