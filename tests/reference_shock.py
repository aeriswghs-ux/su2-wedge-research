"""Frozen v1.0 measurement for regression and timing comparisons."""
import numpy as np
from wedgeverify.shock import solve_weak_shock
theory=solve_weak_shock(2,10).as_dict()
def shock_fit(d, fraction):
    x,y=d['Points'][:,:2].T
    p=d['Pressure']
    threshold=100000*(1+fraction*(theory['p2_p1']-1))
    points=[]
    for xx in np.unique(x):
        if not .8<=xx<=1.25: continue
        ids=np.flatnonzero(x==xx); ids=ids[np.argsort(y[ids])]
        for a,b in zip(ids[:-1],ids[1:]):
            if p[a]>=threshold and p[b]<threshold:
                yy=y[a]+(threshold-p[a])*(y[b]-y[a])/(p[b]-p[a])
                points.append((xx,yy))
    points=np.array(points)
    if len(points)<5: raise ValueError('Too few shock crossings')
    slope,intercept=np.polyfit(points[:,0]-.5,points[:,1],1)
    return float(np.degrees(np.arctan(slope))),float(intercept),points

