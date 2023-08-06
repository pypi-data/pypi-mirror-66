import numpy as np
from .clients import FlaskClient, RedisClient
from jarvis.utils.general import printd

def print_url():

    URL = 'http://%s:%s/?user=%s' % (
        fc.configs['host'],
        fc.configs['port'],
        rc.user)

    print('Connect to viewer URL: %s' % URL, end=' ')

    # --- Attempt to display HTML link in IPython / Jupyter
    try:
        from IPython.core.display import display, HTML
        display(HTML('<a href="%s">link</a>' % URL))
    except: pass

def prepare_arr(arr, key):
    """
    Method to prepare arr 

    """
    # --- Return path strings 
    if type(arr) is not np.ndarray:
        return arr 

    # --- Expand 4D
    if arr.ndim == 0:
        arr = np.expand_dims(arr, 0)

    if arr.ndim == 1:
        arr = np.expand_dims(arr, 0)

    if arr.ndim == 2:
        arr = np.expand_dims(arr, 0)

    if arr.ndim == 3:
        arr = np.expand_dims(arr, -1)

    # --- Prepare dtype
    if key == 'dat': 

        # --- Scale to [0, 1000]
        if arr.dtype.name.find('float') > -1:
            arr = arr - arr.min()
            arr = (arr / arr.max() * 1000).astype('int16')

        else:
            arr = arr.astype('int16')

    if key == 'lbl': 
        arr = arr.astype('uint8')

    return arr[..., :1]

def parse_args(*args):
    """
    Method to extract out data / labels from input arguments

    """
    arrs = {}

    # --- Extract Jarvis arrays
    extract_data = lambda x : x.data if type(x) is not np.ndarray and hasattr(x, 'data') else x
    args = [extract_data(a) for a in args]

    if len(args) == 1:

        # --- Assume {'dat': ..., 'lbl': ...}
        if type(args[0]) is dict:
            assert 'dat' in args[0], 'ERROR dict must have key `dat`'
            arrs['dat'] = args[0].get('dat')
            arrs['lbl'] = args[0].get('lbl') 

        # --- Assume that arr is dat
        elif type(args[0]) is np.ndarray:
            arrs['dat'] = args[0]

        # --- Assume that arr is path name
        elif type(args[0]) is str:
            arrs['dat'] = args[0]

    elif len(args) == 2:

        # --- Assume arr is dat then lbl
        if type(args[0]) is np.ndarray and type(args[1]) is np.ndarray:
            arrs['dat'] = args[0]
            arrs['lbl'] = args[1]

        elif type(args[0]) is str and type(args[1]) is str:
            arrs['dat'] = args[0]
            arrs['lbl'] = args[1]

    # --- Prepare
    for k in arrs:
        arrs[k] = prepare_arr(arrs[k], k)

    return {k: arr for k, arr in arrs.items() if arr is not None} 

def parse_kwargs(**kargs):
    """
    Method to extract out data / labels from input arguments

    """
    pass

def show(*args, **kwargs):
    """
    Method to show array in viewer

    """
    # --- Extract data / labels
    arrs = parse_args(*args) or parse_kwargs(**kwargs)

    if len(arrs) == 0:
        return

    # --- Send arrays in redis
    fnames = rc.send_arrs(arrs)

    # --- Post 
    fc.post({'fnames': fnames, 'user': rc.user})

    # --- Grab label
    update = kwargs.get('update', False)
    if update:
        input('Navigate to viewer > update label > press F9 ... [press any key to continue]')
        arr, _ = rc.get_arr_meta(fnames['lbl'][8:])

        return arr

# ================================================================
# INITIALIZE SHOW CLIENT
# ================================================================
rc = RedisClient(host='localhost', port=7787, prefix='JARVIS_REDIS')
fc = FlaskClient(host='localhost', port=7000, prefix='JARVIS_FLASK')
print_url()
# ================================================================
