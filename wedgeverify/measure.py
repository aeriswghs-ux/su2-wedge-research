"""Shared measurements from real flow fields. Coordinates are in metres."""
import numpy as np


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
