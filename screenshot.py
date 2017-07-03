import sys
import os
import Image
import cv2
import numpy as np

""" Local TODOs """
# TODO: duration of imports when imported locally? (eg. in function)
# TODO: further refactor __init__

class Screenshot:
    """
      Basic idea taken from https://stackoverflow.com/questions/69645/take-a-screenshot-via-a-python-script-linux
      Modifications made:
        1) Changed design to return the screenshot as OpenCV / numpy array instead of PIL image format.
        2) Rewrote the horribly designed constructor (__init__)
        3) Fixed the problem with segmentation faults if using Qt to take screenshots.
    """
    def __init__(self):
        # TODO: make a dict containing (libray, function) pairs and use eval() function to import the correct one
        # TODO: duration of imports when imported locally? (eg. in function)
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
          print 'Screenshots cannot be taken on this computer'
          self.screen = None
        else:    
          # wrapper to return the image as OpenCV / numpy array
          self.screenshot = lambda: cv2.cvtColor(np.array(self.screen_()), cv2.COLOR_RGB2BGR)


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
        if Screenshot.qtAppInstance is None:
          Screenshot.qtAppInstance = QApplication(sys.argv)
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


