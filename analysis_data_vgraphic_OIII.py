import library_prop as lib
#import proplyds as prop
import pyfits
import numpy as np
import matplotlib.pyplot as plt
import argparse

#First. Get the information of your fits file (Header + data)
#I'm not so fool to enter a file without a header



#Old fashioned way:
#path1 = raw_input("Enter the path of your fits file  ")
#filename = raw_input("Enter the name of your fits file  ")

#Argparse way:

#Important note: you can write " " with unicode utf-8 using U+0022

parser = argparse.ArgumentParser(description="Input image, coords names and paths")

parser.add_argument("--image","-i",default = "10_wjh_hdr.fits",type=str, help="Fits image file")
parser.add_argument("--coords","-c",default = "ODellWongTable2.fits",type=str, help="Fits table with the coordinates of the proplyds")
parser.add_argument("--path","-p",default = "/fs/computo21/other0/jtarango/todo_python/",type=str, help="Path of fits image file")
parser.add_argument("--path2","-q",default = "/fs/computo21/other0/jtarango/todo_python/",type=str, help="path of fits table")
parser.add_argument("--theta", "-t", default=90.0, type=float, help="Angle of slit (degrees)")
#parser.add_argument("--proplyd", "-P", default="168-326", type=str, help="Name of proplyd")
parser.add_argument("-propx","-P", default = 83.81977, type = float, help= "Right ascension of proplyd")
parser.add_argument("-propy","-Q", default = -5.39054, type = float, help= "Declination of proplyd")
parser.add_argument("--width","-w",default = 1.0,type = float,help = "Width of slit (Arcseconds)")
parser.add_argument("--xmin","-x",default = -80.0,type=float, help="minimal value in x axis")
parser.add_argument("--xmax","-X",default = 100.0,type=float, help="max value in x axis")
parser.add_argument("--ymin","-y",default = -0.001,type=float, help="minimal value in y axis")
parser.add_argument("--ymax","-Y",default = 10.0,type=float, help="max value in y axis")
cmdargs = parser.parse_args()

Filename = cmdargs.image
path1 = cmdargs.path
path2 = cmdargs.path2
#Prop = cmdargs.proplyd

header,data = lib.inputs(path1,Filename)

#Second: Make my X,Y coordinates:

X,Y,dx,dy = lib.XY(header)

#Third: Load the fits file with the table of coordinates of proplyds

#path2 = raw_input("Enter the path of the fits file from O'Dell & Wong  ")

#ra,dec,names = prop.ra_dec_prop(path=path2,filename=cmdargs.coords)

#Fourth: Get the coordinates of my proplyds respect my XY coordinates
#RA grows in the same direction than X and Dec in the same direction as Y

#xpr0,ypr0 = (ra - header['CRVAL1'])*3600.,(dec-header['CRVAL2'])*3600.



Xpr0_beta,Ypr0_beta = (cmdargs.propx - header['CRVAL1'])*3600.,(cmdargs.propy- header['CRVAL2'])*3600.

THETA = np.arctan2(Ypr0_beta,Xpr0_beta) + cmdargs.theta*np.pi/180


#The time of truth...

#Emergency modification:For OIII image, we'll center the slits in any point instead of the coords from O'Dell & Wong due to the systematic displacement
#of proplyds in the OIII image
Ps,Br = lib.slit(data,X,Y,Xpr0_beta,Ypr0_beta,ths=THETA,w=cmdargs.width,delta = dx )

#centering to create an histogram

Pscen = 0.5*(Ps[1:]+Ps[:-1])

xm = cmdargs.xmin
XM = cmdargs.xmax
ym = cmdargs.ymin
YM = cmdargs.ymax

plt.plot(Pscen,Br)
plt.axis([xm,XM,ym,YM]) #Adjusting axes
plt.xlabel('xslit(arcseconds)')
plt.ylabel('Brightness')
plt.title('Histograma') 
plt.savefig('Grafica.png')
plt.clf()




