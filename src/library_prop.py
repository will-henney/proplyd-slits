# -*- coding: utf-8 -*- 
u"""
Demostración de funciones en python
"""



#def squared(x):
#    "Devolver el valor cuadrado del argumento"
#    return x**2



#def power(x, n=2):
#    "Calcular potencia n (default=2) del argumento x"
#    return x**n


#print "El valor de 4 cuadrado es", power(4)
#print "El valor de 4 al cubo es", power(4, 3)
#########################################################################################################################################################

import numpy as np
import pyfits
from matplotlib import pyplot as plt

def slit(Image, X, Y, xs, ys, ths=0.0, w=1.0, delta=1.0):
    """
    Calculate slit profile in an image.

    Input parameters:

       Image : 2D array of brightnesses
       X     : 2D array of x coordinates
       Y     : 2D array of y coordinates

       xs, ys : reference position on slit 
       ths    : orientation angle of slit 
       w      : width of slit in same units as X, Y
       delta  : bin width in same units as X, Y

    Return parameters:

       Position: 1D array of spatial coordinate along slit
                 with respect to the reference position, in same units
                 as X, Y, and with pixel size delta
       Brightness: 1D array of brightness along slit (averaged
                   over slit width)
    """
    # Body of the function ******************************************************************************************************************
    #It's a rectangular slit
    #1st step: set the coordinates of the slit (U,V), U & V are cartesian coordinates but with a rotation. The rotation angle is ths
      
    U = (X - xs)*np.cos(ths) + (Y - ys)*np.sin(ths)
    V = -(X - xs)*np.sin(ths) + (Y - ys)*np.cos(ths)

    #2nd step: set the width of the slit

    M = np.abs(V) < 0.5*w

    #3rd step: set the number of bins

    nbins = np.abs( ( U.max() - U.min() )/( delta ) )

    #3rd step making the histogram

    Brightness,Position = np.histogram(U[M],bins= nbins,weights = Image[M])
    # normalize to give average brightness across slit
    BrightnessNN,Position = np.histogram(U[M], bins=nbins)
    Brightness /= BrightnessNN #Corrected
    return Position, Brightness


def inputs(path,Filename):

    """
    Input parameters: 
    path: character string, set the path to your fits file
    filename: Name of your fits file (also a character string)
 
    Return values:
    headers: all the information about the header of your file
    data: 2D array of brightness
    """
    f=pyfits.open(path+Filename)
    headers=f[0].header
    data=f[0].data
    return headers,data
    

def XY(header):
    """
    This functions take header's data (specifically the dimensions of the image, pixel's size and position of the reference pixel)
    and creats an XY array
    
    Input parameters:
    header: Header of the fits file.
    
    Returns: X,Y (2D arrays with coordinates of the pixels in arcseconds), and dx,dy. Resolution of pixels in x and y, respectively 
    """
    nx,ny = header['NAXIS1'],header['NAXIS2']
    xp = np.array(np.arange(nx)) #modification 2
    yp = np.array(np.arange(ny)) #modification 3
    XP,YP = np.meshgrid(xp,yp)
    xp0 = header['CRPIX1']
    yp0 = header['CRPIX2']
    # x0 = hdr['CRVAL1']
    # y0 = hdr['CRVAL2']

    # world coordinates with origin at reference pixel
    x0 = 0.0
    y0 = 0.0

    # Give priority to CD1_1 keyword if it exists
    try:
        dx = header['CD1_1']*3600.
        dy = header['CD2_2']*3600.
    except KeyError:
        # otherwise try to use the CDELT1 keyword instead
        dx = header['CDELT1']*3600.
        dy = header['CDELT2']*3600.
        
        
    X = (XP - xp0)*dx  
    Y = (YP - yp0)*dy  

    return X,Y,dx,dy

#p = raw_input("Enter the path of your fits file(example: /home/user/my_folder/): ")
  #'/home/jtarango/Dropbox/ProplydMIR/MIR/Robberto/' #Could be useful make that the user enters these inputs
#fn = raw_input("Enter the name of your fits file(example: image.fits):")#'10_wjh_hdr.fits'

#hdr,dat = inputs(p,fn)

#X,Y = XY(hdr)

#pos, brigh = slit(dat,X,Y,0,0,1.73,10)

#cen = 0.5*( pos[1:] + pos[:-1] )

#plt.plot(cen,brigh,':')
#plt.xlabel('position(arcsec)')
#plt.ylabel('brightness')
#plt.title('2nd histogram')
#plt.savefig('slit_hist2.png')


def plotter(xaxis,yaxis,xlow=0,xhigh=100,ylow=0,yhigh=100,picname="grafica.png",xlab="x",ylab="y",pltit="y vs x"):
    """
    This function makes a graph with matplot library.

    Input parameters:

    xaxis: X axis data (array)
    yaxis: Y axis data (array)
    xlow,ylow: lowest value in X axis and Y axis, respectively
    xhigh, yhigh : Highest value of X axis and Y axis
    picname: Name of the output graph (example: 'sine.png')
    xlab: label of X axis
    ylab: label of Y axis
    pltit: Title of the graph (example: 'sin(x) vs x')
    (So far we don't need anymore)
    """

    plt.plot(xaxis,yaxis)
    plt.axis([xlow,xhigh,ylow,yhigh])
    plt.xlabel(xlab)
    plt.ylabel(ylab)
    plt.title(pltit)
    plt.savefig(picname)
    plt.clf()
    return 











































































































































