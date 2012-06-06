import library_prop as lib
import proplyds as prop
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

#Important note: you can write " " with unicode utf-8 usng U+0022

parser = argparse.ArgumentParser(description="Input image, coords names and paths")

parser.add_argument("--image","-i",default = "10_wjh_hdr.fits",type=str, help="Fits image file")
parser.add_argument("--coords","-c",default = "ODellWongTable2.fits",type=str, help="Fits table with the coordinates of the proplyds")
parser.add_argument("--path","-p",default = "/fs/computo21/other0/jtarango/todo_python/",type=str, help="Path of fits image file")
parser.add_argument("--path2","-q",default = "/fs/computo21/other0/jtarango/todo_python/",type=str, help="path of fits table")
parser.add_argument("--theta", "-t", default=90.0, type=float, help="Angle of slit (degrees)")
parser.add_argument("--proplyd", "-P", default="168-326", type=str, help="Name of proplyd")
parser.add_argument("--width","-w",default = 1.0,type = float,help = "Width of slit (Arcseconds)")
parser.add_argument("--xmin","-x",default = -80.0,type=float, help="minimal value in x axis")
parser.add_argument("--xmax","-X",default = 100.0,type=float, help="max value in x axis")
parser.add_argument("--ymin","-y",default = -0.001,type=float, help="minimal value in y axis")
parser.add_argument("--ymax","-Y",default = 10.0,type=float, help="max value in y axis")
cmdargs = parser.parse_args()

Filename = cmdargs.image
path1 = cmdargs.path
path2 = cmdargs.path2
Prop = cmdargs.proplyd

header,data = lib.inputs(path1,Filename)

#Second: Make my X,Y coordinates:

X,Y,dx,dy = lib.XY(header)

#Third: Load the fits file with the table of coordinates of proplyds

#path2 = raw_input("Enter the path of the fits file from O'Dell & Wong  ")

ra,dec,names = prop.ra_dec_prop(path=path2,filename=cmdargs.coords)

#Fourth: Get the coordinates of my proplyds respect my XY coordinates
#RA grows in the same direction than X and Dec in the same direction as Y

xpr0,ypr0 = (ra - header['CRVAL1'])*3600.,(dec-header['CRVAL2'])*3600.

#Fifth: Start to create slits. Let's create a correlation between te proplyd's name and it's positions
#It might be a dictionary. At least for the proplyds from Bally et al. 1998

#This should work

catalogx = {names[s]:xpr0[s] for s in np.arange(np.size(names))}
catalogy = {names[s]:ypr0[s] for s in np.arange(np.size(names))}


#The sintaxis to make all the slits I want:

# slit1,brightness1 = slit(data,X,Y,catalogx["name of the proplyd"],catalogy["name of the proplyd"],ths=value of the angle,w = width of slit, delta = dx)   

#After getting data, we should save it (in file or in a plot)

#in file:
#saving = open("output.dat","w")
#[saving.write(slit[s],brightness[s]) for s in np.arange(size(slit))]  ? Will this work?
#saving.close()

#The other choice is to make a plot ...

#Making 1st Test...

#I have to choose an angle, it'll be the angular position of the proplyd ths = np.arctan2(ys,xs)
#The test proplyd is LV1 (168-326)

THETA = np.arctan2(catalogy[Prop],catalogx[Prop]) + cmdargs.theta*np.pi/180

#thsLV1 = np.arctan2(catalogy['168-326'],catalogx['168-326'])
#print thsLV1*180/np.pi

#The time of truth...
Ps,Br = lib.slit(data,X,Y,catalogx[Prop],catalogy[Prop],ths=THETA,w=cmdargs.width,delta = dx )

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

#Well, let me try to save the Data in file.

#outdata = open('output.dat','w')

#First lines are the Title of textfile and the labels of the axes. Use the program of your preference for graphs
#outdata.write('#Slit centered in proplyd '+ cmdargs.proplyd + ' with angle ' + str(cmdargs.theta)+'width='+str(cmdargs.width)+'\n')
#outdata.write('#Position'+'\t'+'Brightness'+'\n')
#for i in range(0,Br.size):
#    outdata.write( str( Ps[i] )+'\t'+str( Br[i] )+'\n' )

#outdata.close()


