import os
import glob as glb
from itertools import product

def glob(*fs):
    return glb.glob(os.path.join(*fs))

def iglob(*fs):
    return glb.iglob(os.path.join(*fs))

def sglob(*fs):
    return sorted(iglob(*fs))


def pathprod(*parts):
    '''Join path as a product of all components passed.

    Arguments:
        *parts (str, tuple): file path parts - if tuple, it will match each in a product
            of all tuples.
            e.g.:
                fs = pathprod(('tmp', 'tmp2'), 'data', ('{}.csv', '{}.wav'))
                # equivalent to:
                fs = (
                    os.path.join('tmp/data/{}.csv') +
                    os.path.join('tmp/data/{}.wav') +
                    os.path.join('tmp2/data/{}.csv') +
                    os.path.join('tmp2/data/{}.wav'))
    '''
    return [os.path.join(*fp) for fp in product(*[as_tuple(p) for p in parts])]

def prodglob(*parts):
    '''Return list of files matching a product of all path components passed.
    See pathprod for usage.'''
    return list(prodiglob(*parts))

def prodiglob(*parts):
    '''Return a generator of files matching a product of all path components passed.
    See pathprod for usage.'''
    return (f for fp in pathprod(*parts) for f in glb.iglob(fp))

def prodmake(*parts):
    '''Create all directories matching a product of all path components passed.
    See pathprod for usage.'''
    fs = pathprod(*parts)
    for f in fs:
        os.makedirs(f, exist_ok=True)
    return fs

def as_tuple(v):
    '''Convert to tuple. If not a list or tuple, it will return (v,).'''
    return (
        v if isinstance(v, tuple) else
        tuple(v) if isinstance(v, list) else (v,))
