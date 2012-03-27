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
parser.add_argument("--theta", "-t", default=90.0, type=float, help="Angle of slit")
parser.add_argument("--proplyd", "-P", default="168-326", type=str, help="Name of proplyd")

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
Ps,Br = lib.slit(data,X,Y,catalogx[Prop],catalogy[Prop],ths=THETA,delta = dx )

#centering to create an histogram

Pscen = 0.5*(Ps[1:]+Ps[:-1])

lib.plotter(Ps,Br,xlow=-20,ylow=-20,xlab='xslit(arcseconds)',ylab='yslit(arcseconds)')

#plt.plot(PcenLV1,SLV1)
#plt.axis([-20,20,0,300]) #Adjusting axes
#plt.xlabel('xslit(arcseconds)')
#plt.ylabel('yslit(arcseconds)')
#plt.title('Histograma LV1')
#plt.savefig('LV1_b.png')
#plt.clf()
#repeat everything with a perpendicular slit
#thsLV1_n = thsLV1 + 0.5*np.pi
#print thsLV1_n*180/np.pi

#PnLV1,SnLV1 = lib.slit(data,X,Y,catalogx['168-326'],catalogy['168-326'],ths = thsLV1_n,w = 2.5,delta = dx)
#PncenLV1 = 0.5*(PnLV1[1:]+PnLV1[:-1])

#plt.plot(PncenLV1,SnLV1)
#plt.axis([-20,20,0,300]) #Adjusting axes
#plt.xlabel('xslit(arcseconds)')
#plt.ylabel('yslit(arcseconds)')
#plt.title('Histograma LV1 (normal)')
#plt.savefig('LV1n_b.png')
#plt.clf()

#Must try with LV3
#Once being sure about the angle, let's proceed with LV3 (The slit that passes through Th1C and the normal one)

#thsLV3 = np.arctan2(catalogy['163-317'],catalogx['163-317'])
#thsLV3_n = thsLV3 + 0.5*np.pi

#PLV3,SLV3 = lib.slit(data,X,Y,catalogx['163-317'],catalogy['163-317'],ths =thsLV3, w = 2.5,delta = dx)
#PnLV3,SnLV3 = lib.slit(data,X,Y,catalogx['163-317'],catalogy['163-317'],ths =thsLV3_n, w = 2.5,delta = dx)

#The plots ...
#PcenLV3 = 0.5*(PLV3[1:]+PLV3[:-1])
#PncenLV3 = 0.5*(PnLV3[1:]+PnLV3[:-1])

#plt.plot(PcenLV3,SLV3)
#plt.axis([-20,20,0,300]) #Adjusting axes
#plt.xlabel('xslit(arcseconds)')
#plt.ylabel('yslit(arcseconds)')
#plt.title('Histograma LV3')
#plt.savefig('LV3.png')
#plt.clf()

#plt.plot(PncenLV3,SnLV3)
#plt.axis([-20,20,0,300]) #Adjusting axes
#plt.xlabel('xslit(arcseconds)')
#plt.ylabel('yslit(arcseconds)')
#plt.title('Histograma LV3 (normal)')
#plt.savefig('LV3n.png')
#plt.clf()

#I have to find a way to minimize this code
