import numpy as np
import json

# =====================================================
# BINARY PACK / UNPACK
# =====================================================
# 
# The packed binary consists of two parts:
#   
#   (1) JSON object 
#   (2) Numpy array 
# 
# The JSON object is encoded as two parts:
# 
#   (1) 4-byte integer (length of JSON string in bytes)
#   (2) JSON object
# 
# At minimum, the JSON object will contain:
#
#   * dtype
#   * shape
#   * vsize 
#
# =====================================================

def pack(arr, meta=None):
    """
    Method to pack array with meta 

    """
    if meta is None:
        meta = {}

    meta['dtype'] = str(arr.dtype)
    meta['shape'] = arr.shape
    meta['vsize'] = [1, 1, 1] if 'vsize' not in meta else list(meta['vsize'][:3])

    # --- Combine
    meta = bytes(json.dumps(meta), 'utf-8')
    size = np.array(len(meta)).astype('int32')

    return size.tobytes() + meta + arr.tobytes() 

def unpack(b):
    """
    Method to unpack array and meta 

    """
    # --- Meta
    size, meta = unpack_meta(b)

    # --- Array
    arr = np.frombuffer(b[4+size:], dtype=meta['dtype'])
    arr = arr.reshape(meta['shape'])

    if arr.ndim == 3:
        arr = np.expand_dims(arr, -1)

    return arr, meta 

def unpack_meta(b):
    """
    Method to unpack meta ony

    """
    # --- Meta 
    size = int(np.frombuffer(b[:4], dtype='int32'))
    meta = json.loads(str(b[4:4+size], 'utf-8'))

    return size, meta

