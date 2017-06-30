from pymouse import PyMouse
from time import sleep

""" Local TODOs """
# TODO: duration of imports when imported locally? (eg. in function)
# TODO: refactor perform_mouse_drag and shot_vector
# TODO: window shift should be a global variable or singleton?

class GameAreaShift: 
  """
    A Borg class (TODO: link here) containing the shift of the game area
    in screen as (y_shift, x_shift).
  """
  shift = np.int32([0, 0])

def click_play_again(img_screen):
  # TODO: implement this
  pass

def shot_vector(mouse_start, mouse_end):
  # TODO: reduce shot angle when the basket is near the edges
  # TODO: find the mathematical model
  # TODO: this function should take y difference into account
  mend = mouse_end - mouse_start  
  mend[0] *= 0.7
  return mend

def perform_mouse_drag(shift, mouse_start, mouse_end):
  # TODO: this is just ugly => refactor
  m = PyMouse()
  
  m_x, m_y = mouse_start + shift
  m_end_x, m_end_y = mouse_start + shot_vector(mouse_start, mouse_end)
  
  # focus browser
  m.click(m_x, m_y)
  
  m.press(m_x, m_y)
  sleep(0.1)
  m.release(m_end_x, m_end_y)
