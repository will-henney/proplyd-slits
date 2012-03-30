import pyfits
import numpy as np


def ra_dec_prop(path,filename):

    f = pyfits.open(path + filename)
  
    table = f[1].data

    ra_list = [float(s) for s in table._RAJ2000]

    ra = np.array(ra_list) #In degrees

    dec_list = [float(s) for s in table._DEJ2000]

    dec = np.array(dec_list) #In degrees
    
    names = table.__OW94_
    
    return ra,dec,names

