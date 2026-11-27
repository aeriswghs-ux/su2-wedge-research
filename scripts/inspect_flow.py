"""Read SU2 uncompressed appended-raw VTU output without extra dependencies."""
from pathlib import Path
import re
import numpy as np

def read_vtu(path):
    data = Path(path).read_bytes()
    marker = re.search(rb'<AppendedData[^>]*>\s*_', data)
    if marker is None:
        raise ValueError('Expected appended raw VTU')
    header = data[:marker.start()].decode('utf-8')
    if 'compressor=' in header or 'header_type="UInt64"' not in header:
        raise ValueError('Unsupported VTU encoding')
    types = {'Float32':'<f4','Float64':'<f8','Int32':'<i4','UInt8':'u1'}
    arrays = {}
    for tag in re.findall(r'<DataArray\b[^>]*>', header):
        attrs = dict(re.findall(r'(\w+)\s*=\s*"([^"]*)"', tag))
        offset = marker.end() + int(attrs['offset'])
        size = int.from_bytes(data[offset:offset+8], 'little')
        arr = np.frombuffer(data[offset+8:offset+8+size],dtype=types[attrs['type']]).copy()
        n = int(attrs.get('NumberOfComponents',1))
        arrays[attrs['Name'] or 'Points'] = arr.reshape(-1,n) if n>1 else arr
    return arrays

if __name__ == '__main__':
    import sys
    d=read_vtu(sys.argv[1])
    for k,v in d.items():
        print(k, v.shape, float(v.min()), float(v.max()), 'finite', bool(np.isfinite(v).all()))
    x,y=d['Points'][:,:2].T
    region=(x>0.8)&(x<1.2)&(y>0.12)&(y<0.2)
    for k in ['Pressure','Density','Mach']:
        if k in d: print('region',k,float(d[k][region].mean()))
