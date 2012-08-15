import pyfits
import numpy as np

def hms2deg(char):
    """
    Function used to transform the Right Ascension from the fits file given in hours, minutes and seconds
    to degrees.
    Argument: THe RA as a string of characters
    output: A float number: the RA written in degrees
    """
    h,m,s = [float(x) for x in char.split()]
    out = 15*(h+m/60.+s/3600.)
    return out

def dms2deg(char):
    
    """
    Function used to transform the Declination from the fits file given in degrees, minutes and seconds
    to degrees.
    Argument: The dec as a string of characters
    output: A float number: the Dec written in degrees
    """
    d,m,s = [float(x) for x in char.split()]
    m,s = np.copysign(m,d),np.copysign(s,d) # The arcminutes and arcseconds adquire the same sign of degrees to be added later
    out = (d + m/60.+ s/3600.) 
    return out

def ra_dec_prop(path,filename):

    f = pyfits.open(path + filename)
  
    table = f[1].data

    ra_list = table.RA2000
    
    ra = np.array([hms2deg(z) for z in ra_list]) 

    dec_list = table.DE2000
    
    dec = np.array([dms2deg(z) for z in dec_list])   

    names = table.__OW94_
    
    return ra,dec,names

