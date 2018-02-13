#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import numpy as np
import cv2
import sys
import os
import time


def get_cams():
   """Returns a list with all the video devices connected to the computer."""
   aux = os.popen('ls /dev/video*').read().splitlines()
   cams = []
   for c in aux:
      if len(c) > 0: cams.append(c.lstrip().rstrip())
   return cams


def foto(i=1,root='foto'):
   """
     Returns a picture and saves it as a jpg file
   """
   camera_port = i
   cam = cv2.VideoCapture(camera_port)
   img = get_image(cam)
   file_out = "./%s%s.jpg" % (root,camera_port)
   cv2.imwrite(file_out, img)
   cam.release()
   return img


def record(i=1,show=False,fname='/tmp/output.avi',dur=10,siz=20000):
   """ Records a video in a avi file of 10 seconds or 20Mb """
   if os.path.isfile(fname):
      name = fname
      cont = 0
      while os.path.isfile(name[0:-4]+str(cont)+'.avi'):
         cont += 1
      fname = name[0:-4]+str(cont)+'.avi'
   t_ini = time.time()
   cap = cv2.VideoCapture(i)
   fourcc = cv2.cv.CV_FOURCC(*'XVID')
   out = cv2.VideoWriter(fname,fourcc, 20.0, (640,480))
   while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==True:
         frame = cv2.flip(frame,180)
         # write the frame
         out.write(frame)
         # show?
         if show:
            cv2.imshow('frame', frame)
            k = cv2.waitKey(5) & 0xFF  # if cv2.waitKey(1) & 0xFF == ord('q'):
            if k == 27: break
         size = float(os.popen('du %s'%(fname)).read().split()[0])
         duration = time.time()-t_ini
         if os.path.isfile('./STOP'): break
         elif size > siz: break
         elif duration > dur: break
      else: break

   cap.release()
   out.release()
   cv2.destroyAllWindows()



def record1(i=1, show=False):
   """
     Records a video in a avi file
   """
   cap = cv2.VideoCapture(i)
   fourcc = cv2.cv.CV_FOURCC(*'XVID')
   out = cv2.VideoWriter('./output.avi',fourcc, 20.0, (640,480))
   while(cap.isOpened()):
      ret, frame = cap.read()
      if ret==True:
         frame = cv2.flip(frame,180)
         # write the flipped frame
         out.write(frame)
         if show: cv2.imshow('frame', frame)
         else: cv2.imshow('frame',np.array([1,0,0]))
         k = cv2.waitKey(5) & 0xFF  # if cv2.waitKey(1) & 0xFF == ord('q'):
         if k == 27: break
         else: break
   # Release everything if job is finished
   cap.release()
   out.release()
   cv2.destroyAllWindows()


def get_image(camera):
   """
     Extracts a frame of the video stream
   """
   retval, im = camera.read()
   if not retval : sys.exit('ERROR: Error al capturar frame (video.py)')
   return im


if __name__ == '__main__':
   # ===============================================
   #    Check if the laptop lid is open or closed
   # ===============================================
   status = os.popen("cat /proc/acpi/button/lid/LID0/state").read().rstrip('\n').split(':')[1].lstrip().rstrip()
   cams = os.popen("ls /dev/video*").read().rstrip('\n').split('\n')
   myhost = os.uname()[1]

   if status == 'closed':
      ubicacion = cams.index("/dev/video0")
      del cams[ubicacion]
   elif status == 'open': pass
   else:
      print('WARNING: Lid status could not be stablished')
   IDcam = 1

   # ====================
   #    Take a picture
   # ====================
   for cam in cams:
      IDcam = int(cam.split('video')[1])
      A = foto(IDcam,myhost)
