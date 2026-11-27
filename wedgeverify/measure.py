"""Shared measurements from real flow fields. Coordinates are in metres."""
import numpy as np


def gradient_shock(data, interpolate=True):
    """Fit the strongest negative vertical pressure gradient; no theoretical jump.

    Use x=0.8..1.25 m, at least 0.04 m above the known ramp and below y=0.95 m.
    Optional three-point parabolic refinement reduces midpoint quantization.
    """
    xy=data['Points'][:,:2].astype(float)
    pressure=data['Pressure'].astype(float)
    points=[]
    for x in np.unique(xy[:,0]):
        if not .8<=x<=1.25: continue
        ids=np.flatnonzero(xy[:,0]==x);ids=ids[np.argsort(xy[ids,1])]
        y=xy[ids,1];p=pressure[ids]
        if len(y)<4 or np.any(np.diff(y)<=0):raise ValueError('Need distinct, ordered column points')
        mid=(y[:-1]+y[1:])/2;strength=-np.diff(p)/np.diff(y)
        allowed=(mid>max(x-.5,0)*np.tan(np.deg2rad(10))+.04)&(mid<.95)
        candidates=np.flatnonzero(allowed)
        if not len(candidates):continue
        k=candidates[np.argmax(strength[candidates])]
        if not np.isfinite(strength[k]) or strength[k]<=1e-8:continue
        location=mid[k]
        if interpolate and 0<k<len(mid)-1 and allowed[k-1:k+2].all():
            a,b,_=np.polyfit(mid[k-1:k+2]-location,strength[k-1:k+2],2)
            if a<0:
                vertex=location-b/(2*a)
                if mid[k-1]<=vertex<=mid[k+1]:location=vertex
        points.append((x,location))
    if len(points)<5:raise ValueError('Too few pressure-gradient peaks')
    points=np.array(points);slope,intercept=np.polyfit(points[:,0]-.5,points[:,1],1)
    return float(np.degrees(np.arctan(slope))),float(intercept),points


def pressure_crossings(data, pressure_jump, fractions=(.4, .5, .6)):
    """Fit pressure crossings on vertical columns; sort points only once."""
    xy = data['Points'][:, :2]
    order = np.lexsort((xy[:, 1], xy[:, 0]))
    x, y = xy[order].T
    p = data['Pressure'][order]
    same_column = (x[:-1] == x[1:]) & (x[:-1] >= .8) & (x[:-1] <= 1.25)
    fits = []
    for fraction in fractions:
        threshold = 100000 * (1 + fraction * (pressure_jump - 1))
        a = np.flatnonzero(same_column & (p[:-1] >= threshold) & (p[1:] < threshold))
        if len(a) < 5:
            raise ValueError('Too few shock crossings for a reliable line fit')
        crossings = y[a] + (threshold - p[a]) * (y[a+1] - y[a]) / (p[a+1] - p[a])
        slope, intercept = np.polyfit(x[a] - .5, crossings, 1)
        fits.append((float(np.degrees(np.arctan(slope))), float(intercept), np.column_stack((x[a], crossings))))
    return fits


def cell_values(data):
    """Compute cell geometry and field averages once for any number of boxes."""
    cells = data['connectivity'].reshape(-1, 4)
    poly = data['Points'][:, :2].astype(float)[cells]
    area = .5 * np.abs(np.sum(poly[:, :, 0] * np.roll(poly[:, :, 1], -1, axis=1)
                             - poly[:, :, 1] * np.roll(poly[:, :, 0], -1, axis=1), axis=1))
    fields = {key: data[key][cells].mean(axis=1) for key in ['Pressure', 'Density', 'Mach']}
    return poly, poly.mean(axis=1), area, fields


def box_average(centers, area, fields, box):
    x0, x1, y0, y1 = box
    x, y = centers.T
    mask = (x >= x0) & (x <= x1) & (y >= y0) & (y <= y1)
    if not mask.any():
        raise ValueError('Measurement box contains no cell centers')
    return {key: float(np.average(values[mask], weights=area[mask])) for key, values in fields.items()}, int(mask.sum())
