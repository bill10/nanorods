
# coding: utf-8

# In[60]:

import numpy as np
import math
import sys
import pickle
import time


# In[61]:

class Stopwatch(object):
    start_time=None
    def go(self):
        self.start_time=time.time()
        sys.stdout.flush()
    def stop(self):
        print "Elapsed time: %f seconds" % (time.time()-self.start_time)
        sys.stdout.flush()
    def check(self):
        return time.time()-self.start_time


def point2line(x1,y1,x2,y2,x3,y3):
    # (x3,y3) to line (x1,y1)-(x2,y2)
    u=((x3-x1)*(x2-x1)+(y3-y1)*(y2-y1))/((x2-x1)**2+(y2-y1)**2)
    if u>=1:
        return np.linalg.norm((x3-x2,y3-y2))
    elif u<=0:
        return np.linalg.norm((x3-x1,y3-y1))
    else:
        return np.linalg.norm((x1+u*(x2-x1)-x3,y1+u*(y2-y1)-y3))


# In[55]:

nrealizations=100;
r=0.5;
leng=50;
boxleng=10*(leng+2*r);
nrods=int(sys.argv[1]);
cutoff=2*r;
rand=np.random.rand
ntriangles=[]
degrees=[]
print '{} rods'.format(nrods)


# In[56]:

tic=Stopwatch()
tic.go()
for realization in xrange(nrealizations):
    x=rand(nrods)*boxleng;
    y=rand(nrods)*boxleng;
    theta=rand(nrods)*2*math.pi;
    ex=np.cos(theta);
    ey=np.sin(theta);
    degree=np.zeros(x.shape)
    
    adj=dict()
    for i in xrange(len(x)):
        adj[i]=list()
    for i in xrange(len(x)):
        x1,x2=(x[i]-0.5*leng*ex[i],x[i]+0.5*leng*ex[i])
        y1,y2=(y[i]-0.5*leng*ey[i],y[i]+0.5*leng*ey[i])
        for j in xrange(i+1,len(x)):
            x3,x4=(x[j]-0.5*leng*ex[j],x[j]+0.5*leng*ex[j])
            y3,y4=(y[j]-0.5*leng*ey[j],y[j]+0.5*leng*ey[j])
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
            if dij<=2*r:
                adj[i].append(j)
                adj[j].append(i)
                degree[i]+=1
                degree[j]+=1
    
    ntriangle=0
    visited_ids = set()
    for node_a_id in adj:
        for node_b_id in adj[node_a_id]:
            if node_b_id == node_a_id:
                raise ValueError # nodes shouldn't point to themselves
            if node_b_id in visited_ids:
                continue # we should have already found b->a->??->b
            for node_c_id in adj[node_b_id]:
                if node_c_id in visited_ids:
                    continue # we should have already found c->a->b->c
                if node_a_id in adj[node_c_id]:
                    ntriangle+=1
        visited_ids.add(node_a_id) # don't search a - we already have all those cycles
    
    ntriangles.append(ntriangle)
    degrees.append(np.mean(degree))

outfile=open('{}.pkl'.format(nrods),'wb')
pickle.dump((nrods,ntriangles,degrees,tic.check()),outfile)
outfile.close()

