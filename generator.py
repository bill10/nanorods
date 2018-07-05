
# coding: utf-8


import numpy as np
import math
import sys
import pickle
import time


def point2line(x1,y1,x2,y2,x3,y3):
    # (x3,y3) to line (x1,y1)-(x2,y2)
    u=((x3-x1)*(x2-x1)+(y3-y1)*(y2-y1))/((x2-x1)**2+(y2-y1)**2)
    if u>=1:
        return np.linalg.norm((x3-x2,y3-y2))
    elif u<=0:
        return np.linalg.norm((x3-x1,y3-y1))
    else:
        return np.linalg.norm((x1+u*(x2-x1)-x3,y1+u*(y2-y1)-y3))


def GenerateRods():
    x=np.random.rand(nrods)*boxlen;
    y=np.random.rand(nrods)*boxlen;
    theta=np.random.rand(nrods)*2*math.pi;
    ex=np.cos(theta);
    ey=np.sin(theta);
    if filename:
        np.savetxt(filename+'.rods',np.array((x-0.5*rodlen*ex,y-0.5*rodlen*ey,x+0.5*rodlen*ex,y+0.5*rodlen*ey)).T)
    return (x-0.5*rodlen*ex,y-0.5*rodlen*ey,x+0.5*rodlen*ex,y+0.5*rodlen*ey)


def GetNetwork(X1,Y1,X2,Y2):
    if filename:
        outfile=open(filename+'.adj','w')
    adj=dict()
    for i in xrange(len(X1)):
        adj[i]=list()
    for i in xrange(len(X1)):
        x1,y1,x2,y2=(X1[i],Y1[i],X2[i],Y2[i])
        for j in xrange(i+1,len(X1)):
            x3,y3,x4,y4=(X1[j],Y1[j],X2[j],Y2[j])
            d1=point2line(x3,y3,x4,y4,x1,y1)
            d2=point2line(x3,y3,x4,y4,x2,y2)
            d3=point2line(x1,y1,x2,y2,x3,y3)
            d4=point2line(x1,y1,x2,y2,x4,y4)
            dij=np.amin([d1,d2,d3,d4])
            k=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
            if k!=0:
                ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/k
                ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/k
                if ua>=0 and ua<=1 and ub>=0 and ub<=1:
                    dij=0
            if dij<=cutoff:
                adj[i].append(j)
                adj[j].append(i)
                if filename:
                    outfile.write('{} {}\n'.format(i,j))
    if filename:
        outfile.close()
    return adj


r=0.5;
rodlen=50;
boxlen=10*(rodlen+2*r);
nrods=100;
cutoff=2*r;
filename=''

nrods=int(sys.argv[1]);
r=float(sys.argv[2]);
rodlen=float(sys.argv[3]);
boxlen=float(sys.argv[4]);
cutoff=float(sys.argv[5]);
filename=sys.argv[6];

X1,Y1,X2,Y2=GenerateRods();
adj=GetNetwork(X1,Y1,X2,Y2);