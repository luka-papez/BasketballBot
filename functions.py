import cv2
import numpy as np
from pymouse import PyMouse
from time import sleep

# TODO: reduce shot angle when the basket is near the edges
# TODO: find the mathematical model
# TODO: this function should take y difference into account
def shot_vector(mouse_start, mouse_end):
  mend = mouse_end - mouse_start
  
  mend[0] *= 0.7

  return mend

def perform_mouse_drag(mouse_start, mouse_end):
  m = PyMouse()
  
  m_x, m_y = mouse_start
  m_end_x, m_end_y = mouse_start + shot_vector(mouse_start, mouse_end)
  
  # focus browser
  m.click(m_x, m_y)
  
  m.press(m_x, m_y)
  sleep(0.1)
  m.release(m_end_x, m_end_y)

# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_houghcircles/py_houghcircles.html
def find_ball(img_screen, img_dbg = None):
  img_screen_bin = cv2.cvtColor(img_screen, cv2.COLOR_RGB2GRAY)
  # TODO: tweak parameters
  circles = cv2.HoughCircles(img_screen_bin, cv2.HOUGH_GRADIENT, 2, 500, minRadius = 20, maxRadius = 200)
  if circles is None:
    print "Couldn't find circles"
    return None
    
  circles = np.uint16(np.around(circles))
  # no idea why this needs to be done
  circles = circles[0] 

  for i in circles:
      # draw the outer circle
      cv2.circle(img_dbg, (i[0], i[1]), i[2], (0, 255, 0), 2)
      # draw the center of the circle
      cv2.circle(img_dbg, (i[0], i[1]), 2, (0, 0, 255), 3)
  
  # if there are many found circles, sort descending according to circle radius and use the biggest one
  if len(circles) > 1:
    print "Found many circles, this shouldn't happen"
    circles.sort(key=lambda circle: circle[2])

  return circles[0][:-1]

# http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_template_matching/py_template_matching.html
img_basket = cv2.imread('basket.png')
def find_basket(img_screen, img_dbg = None):
  method = cv2.TM_CCOEFF_NORMED
  res = cv2.matchTemplate(img_screen, img_basket, method)
  min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)

  h, w, _ = img_basket.shape
  top_left = np.array(max_loc)
  bottom_right = np.array((top_left[0] + w, top_left[1] + h))

  if img_dbg is not None:
    cv2.rectangle(img_dbg, tuple(top_left), tuple(bottom_right), 255, 2)
  
  return (top_left + bottom_right) / 2

"""
screengrab.py

Created by Alex Snet on 2011-10-10.
Copyright (c) 2011 CodeTeam. All rights reserved.
"""
import sys
import os
import Image

# https://stackoverflow.com/questions/69645/take-a-screenshot-via-a-python-script-linux
class Screengrab:
    def __init__(self):
        imported = False
        
        if not imported:            
          try:
              import PyQt4
          except ImportError:
              pass
          else:
              self.screen_ = self.getScreenByQt
              imported = True
        
        if not imported:
          try:
              import gtk
          except ImportError:
              pass
          else:
              self.screen_ = self.getScreenByGtk
              imported = True
            
        if not imported:
          try:
              import wx
          except ImportError:
              pass
          else:
              self.screen_ = self.getScreenByWx
              imported = True
            
        if not imported:
          try:
              import ImageGrab
          except ImportError:
              pass
          else:
              self.screen_ = self.getScreenByPIL
              imported = True
            
        if not imported:
          print 'Cannot take screenshot on this computer'
          self.screen = None
        else:    
          # wrapper to return the image as OpenCV / numpy array
          self.screen = lambda: cv2.cvtColor(np.array(self.screen_()), cv2.COLOR_RGB2BGR)


    def getScreenByGtk(self):
        import gtk.gdk      
        w = gtk.gdk.get_default_root_window()
        sz = w.get_size()
        pb = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB,False,8,sz[0],sz[1])
        pb = pb.get_from_drawable(w,w.get_colormap(),0,0,0,0,sz[0],sz[1])
        if (pb != None):
            return False
        else:
            width,height = pb.get_width(),pb.get_height()
            return Image.fromstring("RGB",(width,height),pb.get_pixels() )
    
    qtAppInstance = None
    def getScreenByQt(self):
        from PyQt4.QtGui import QPixmap, QApplication
        from PyQt4.Qt import QBuffer, QIODevice
        import StringIO
        # there should only ever be a single instance of QApplication or else it crashes on some platforms
        if Screengrab.qtAppInstance is None:
          Screengrab.qtAppInstance = QApplication(sys.argv)
        buffer = QBuffer()
        buffer.open(QIODevice.ReadWrite)
        QPixmap.grabWindow(QApplication.desktop().winId()).save(buffer, 'png')
        strio = StringIO.StringIO()
        strio.write(buffer.data())
        buffer.close()
        strio.seek(0)
        return Image.open(strio)

    def getScreenByPIL(self):
        import ImageGrab
        img = ImageGrab.grab()
        return img

    def getScreenByWx(self):
        import wx
        wx.App()  # Need to create an App instance before doing anything
        screen = wx.ScreenDC()
        size = screen.GetSize()
        bmp = wx.EmptyBitmap(size[0], size[1])
        mem = wx.MemoryDC(bmp)
        mem.Blit(0, 0, size[0], size[1], screen, 0, 0)
        del mem  # Release bitmap
        #bmp.SaveFile('screenshot.png', wx.BITMAP_TYPE_PNG)
        myWxImage = wx.ImageFromBitmap( myBitmap )
        PilImage = Image.new( 'RGB', (myWxImage.GetWidth(), myWxImage.GetHeight()) )
        PilImage.fromstring( myWxImage.GetData() )
        return PilImage


