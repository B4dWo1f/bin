#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec

try: fnames = sys.argv[1:]
except IndexError:
   print('File to plot not provided')
   exit()

i,j = 0,1
skip = 0

for fname in fnames:
   names = open(fname,'r').readlines()[0]
   if names[0] != '#': names = [None, None]
   else: names = names[1:].split()

   M = np.loadtxt(fname)

   
   if len(names) > 1: names = [names[i],names[j]]
   else: names = ['X','Y']

   X = M[:,i]
   Y = M[:,j]

   X = X[skip:]
   Y = Y[skip:]

   fig = plt.figure()
   gs = gridspec.GridSpec(2, 2)
   fig.subplots_adjust() #wspace=0.1,hspace=0.1)
   ax1 = plt.subplot(gs[0,0])
   ax2 = plt.subplot(gs[0,1])
   ax3 = plt.subplot(gs[1,0])
   ax4 = plt.subplot(gs[1,1])

   ## X-Y
   #################
   from scipy.optimize import curve_fit
   def f(x,a,b):
      return a/(x**b)
   fit,_ = curve_fit(f,X,Y)
   #################
   x= np.linspace(min(X),max(X),100)
   ax1.plot(X,Y,'o-')
   ax1.plot(x,f(x,*fit),'k--')
   ax1.set_title('$%.3f/x^{%.3f}$'%(fit[0],fit[1]))
   if all(n != None for n in names):
      print('**')
      ax1.set_ylabel(names[1])
      ax1.set_xlabel(names[0])
   ax1.grid()

   errores = []
   ## log(X)-Y
   fit = np.polyfit(np.log(X),Y,1)
   x = np.linspace(min(np.log(X)),max(np.log(X)),100)
   p = np.poly1d(fit)
   ax2.plot(np.log(X),Y,'o-')
   ax2.plot(x,p(x),'k--')
   ax2.set_title('$%.4f\cdot x%+.4f$'%(fit[0],fit[1]))
   if all(n != None for n in names):
      ax2.set_ylabel(names[1])
      ax2.set_xlabel('log('+names[0]+')')
   ax2.grid()
   YY = p(np.log(X))
   err = np.sum( [(Y[i] - YY[i])**2 for i in range(len(Y))] )
   errores.append(err)
   print('logx,y',err)

   ## X-log(Y)
   fit = np.polyfit(X,np.log(Y),1)
   x = np.linspace(min(X),max(X),100)
   p = np.poly1d(fit)
   ax3.plot(X,np.log(Y),'o-')
   ax3.plot(x,p(x),'k--')
   ax3.set_title('$%.4f\cdot x%+.4f$'%(fit[0],fit[1]))
   if all(n != None for n in names):
      ax3.set_ylabel('log('+names[1]+')')
      ax3.set_xlabel(names[0])
   ax3.grid()
   YY = p(X)
   err = np.sum( [(Y[i] - YY[i])**2 for i in range(len(Y))] )
   errores.append(err)
   print('x,logy',err)

   ## log(X)-log(Y)
   fit = np.polyfit(np.log(X),np.log(Y),1)
   x = np.linspace(min(np.log(X)),max(np.log(X)),100)
   p = np.poly1d(fit)
   ax4.plot(np.log(X),np.log(Y),'o-')
   ax4.plot(x,p(x),'k--')
   ax4.set_title('$%.4f\cdot x%+.4f$'%(fit[0],fit[1]))
   if all(n != None for n in names):
      ax4.set_ylabel('log('+names[1]+')')
      ax4.set_xlabel('log('+names[0]+')')
   ax4.grid()
   YY = p(np.log(X))
   err = np.sum( [(Y[i] - YY[i])**2 for i in range(len(Y))] )
   errores.append(err)
   ind = errores.index(min(errores))+1
   print('logx,logy',err)
   print('')
   print('minimum error in plot:',ind) #errores.index(min(errores))+1)
   funcs = ['y = a*log(x)+b','y=e^(ax+b)','y=x^a+e^b']
   print('Most probable dependence:')
   print(funcs[ind-1])

   fig.tight_layout()
plt.show()
