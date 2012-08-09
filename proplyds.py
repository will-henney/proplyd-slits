import pyfits
import numpy as np


def ra_dec_prop(path,filename):

    f = pyfits.open(path + filename)
  
    table = f[1].data

    ra_list = table.RA2000
    
    ra_split = ra_list.split()

    hour = [float(ra_split[x][0]) for x in np.arange(np.size(ra_list))]
    minute = [float(ra_split[x][1]) for x in np.arange(np.size(ra_list))]
    second = [float(ra_split[x][2]) for x in np.arange(np.size(ra_list))]

    hr,mn,sec = np.array(hour), np.array(minute),np.array(second)
     

    ra = 15*(hr + mn/60. + sec/3600.) #In degrees

    dec_list = table.DE2000

    dec_split = dec_list.split() 

    degree = [float(dec_split[x][0]) for x in np.arange(np.size(dec_list))]
    arcminute = [float(dec_split[x][1]) for x in np.arange(np.size(dec_list))]
    arcsecond = [float(dec_split[x][2]) for x in np.arange(np.size(dec_list))]

    deg,amin,asec = np.array(degree), np.array(arcminute),np.array(arcsecond)

    amin = np.copysign(amin,deg)  # The arcminutes and arcseconds adquire the same sign of degrees to be added later
    asec = np.copysign(asec,deg)
    
    dec = (deg + amin/60. + asec/3600.) #In degrees     

    names = table.__OW94_
    
    return ra,dec,names

