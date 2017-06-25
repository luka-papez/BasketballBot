import cv2
import numpy as np
from pymouse import PyMouse
from time import sleep

def perform_mouse_drag(mouse_start, mouse_end):
  m = PyMouse()
  
  m_x, m_y = mouse_start
  m_end_x, m_end_y = (mouse_end - mouse_start) / 2 + mouse_start
  
  # focus browser
  m.click(m_x, m_y)
  
  #m.drag(m_x, m_y, m_end_x, m_end_y)
  print 'Dragging', m_x, m_y, m_end_x, m_end_y
  m.press(m_x, m_y)
  sleep(0.05)
  m.release(m_end_x, m_end_y)
  
  sleep(0.05)
  m.move(1500, 800)

# encoding: utf-8
"""
screengrab.py

Created by Alex Snet on 2011-10-10.
Copyright (c) 2011 CodeTeam. All rights reserved.
"""
import sys
import os
import Image
from PyQt4.QtGui import QPixmap, QApplication
from PyQt4.Qt import QBuffer, QIODevice
import StringIO
class screengrab:
    def __init__(self):
        
        try:
            import PyQt4
        except ImportError:
            pass
        else:
            self.screen_ = self.getScreenByQt
        
        # wrapper to return the image as OpenCV
        self.screen = lambda: cv2.cvtColor(np.array(self.screen_()), cv2.COLOR_RGB2BGR)
        # app should be created only once
        self.app = QApplication(sys.argv)
        
    def getScreenByQt(self):
        buff = QBuffer()
        buff.open(QIODevice.ReadWrite)
        QPixmap.grabWindow(QApplication.desktop().winId()).save(buff, 'png')
        strio = StringIO.StringIO()
        strio.write(buff.data())
        buff.close()
        strio.seek(0)
        return Image.open(strio)


# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
def find_ball(img_screen, img_dbg = None):
  img_screen_bin = cv2.cvtColor(img_screen, cv2.COLOR_RGB2GRAY)
  # TODO: tweak parameters
  circles = cv2.HoughCircles(img_screen_bin, cv2.HOUGH_GRADIENT, 2, 500, minRadius = 10, maxRadius = 100)
  if circles is None:
    print "Couldn't find circles"
    return None
    
  circles = np.uint16(np.around(circles))

  for i in circles[0,:]:
      # draw the outer circle
      cv2.circle(img_dbg, (i[0], i[1]), i[2], (0, 255, 0), 2)
      # draw the center of the circle
      cv2.circle(img_dbg, (i[0], i[1]), 2, (0, 0, 255), 3)
  
  if len(circles) > 1 or circles is None:
    print "Found many circles, this shouldn't happen"

  return circles[0][0][:-1]

# TODO: this should be done using template matching and not feature matching
img_basket = cv2.imread('basket.png')
def find_basket(img_screen, img_dbg = None):
  pts_object = find_object_points(img_basket, img_screen)

  object_center = np.int32(np.average(pts_object, axis = 0))
  if img_dbg is not None:
    cv2.circle(img_dbg, (object_center[0], object_center[1]), radius = 2, color = (0, 255, 0), thickness = 2)
  return object_center

# http://docs.opencv.org/trunk/dc/dc3/tutorial_py_matcher.html
def find_object_points(img1, img2, thresh = 0.9):

  # Initiate ORB detector
#  det = cv2.ORB_create()
  det = cv2.BRISK_create()

  # find the keypoints and descriptors 
  kp1, des1 = det.detectAndCompute(img1, None)
  kp2, des2 = det.detectAndCompute(img2, None)
  
  crossCheck = False
      
  # FLANN parameters for ORB and BRISK
  FLANN_INDEX_LSH = 6
  index_params= dict(algorithm = FLANN_INDEX_LSH, table_number = 12, key_size = 15, multi_probe_level = 2) 
  search_params = dict(checks=10000)   # or pass empty dictionary
  matcher = cv2.FlannBasedMatcher(index_params, search_params)
  

  # Match descriptors.
  matches = []
  good = []
  # Need to draw only good matches, so create a mask
  matchesMask = []
  if crossCheck:
    matches = matcher.match(des1, des2)
    good = matches
  else:
    matches = matcher.knnMatch(des1, des2, k = 2)
    matchesMask = [[0,0] for i in xrange(len(matches))]
    # ratio test as per Lowe's paper
    for i, (m, n) in enumerate(matches):
      if m.distance < thresh * n.distance:
        matchesMask[i] = [1,0]
        good.append(m)
  
    
  if len(good) < 10:
    return None
      
  # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html        
  pts_src = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,2)
  pts_dst = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,2)
    
  return pts_dst
