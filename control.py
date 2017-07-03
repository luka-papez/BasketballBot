import numpy as np

def determine_next_basket_position(trajectory, basket_current):
  if len(trajectory) == 0:
    return basket_current
  # TODO: docs
  # find the point in trajectory closest to the current point
  distances = map(lambda x: np.linalg.norm(x - basket_current), trajectory)
  closest_index = distances.index(min(distances))

  # return the next one after the closest
  # TODO: this is dependent on the sampling rate
  return trajectory[(closest_index - 3) % len(trajectory)]

def patterns_overlap(first_pattern, current_pattern):
  # TODO: docs
  # TODO: maybe a more analytical algorithm exists?
  if len(first_pattern) != len(current_pattern):
    # tracking is still not fully initialized
    return False
  else:
    # arbitrary heuristic
    num_close = 0
    for p1, p2 in zip(first_pattern, current_pattern):
      if points_are_close(p1, p2):
        num_close = num_close + 1
    
    # again arbitrary
    return num_close > len(first_pattern) * 0.8

CLOSE_THRESHOLD = 10
def points_are_close(first, second):
  # arbitrary heuristic
  return np.linalg.norm(first - second) < CLOSE_THRESHOLD
