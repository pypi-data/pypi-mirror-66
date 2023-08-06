import numpy as np
import time
from .clients import RedisClient
from .npack import *
from jarvis.utils import io
from jarvis.utils.db import DB, funcs

class IO():

    def __init__(self, HOST='redis', PORT=6379, TIMEOUT=2):

        self.LOAD_FUNCS = {
            'redis': self.load_redis,
            'local': self.load_local}

        self.SAVE_FUNCS = {
            'redis': self.save_redis,
            'local': self.save_local}

        self.TIMEOUT = TIMEOUT
        self.rc = RedisClient(HOST, PORT)

    # ===================================================
    # LOAD FUNCTIONS
    # ===================================================

    def load(self, fname):

        protocol, fname = fname.split('://')

        if protocol in self.LOAD_FUNCS:
            return self.LOAD_FUNCS[protocol](fname)

    def load_redis(self, fname):

        return self.rc.get_buf(fname)

    def load_local(self, fname): 

        buf = None

        data, meta = io.load(fname, verbose=False)

        if data is None:
            data = np.array([[[[]]]], dtype='uint8')
            meta = {}

        meta = self.prepare_meta(meta, fname)
        buf = pack(data, meta)

        return buf 

    def prepare_meta(self, meta, fname):
        """
        Method to prepare meta for viewer

          (1) Parse fname
          (2) Parse vsize
          (3) Parse coord

        """
        # --- Prepare default values
        m = {
            'fname': 'local://{}'.format(fname),
            'vsize': [1, 1, 1],
            'coord': None}

        # --- HDF5 files
        if 'affine' in meta:

            m['vsize'] = np.sqrt(np.sum(meta['affine'][:3, :3] ** 2, axis=0)).tolist()
            m['coord'] = {'affine': meta['affine'].ravel()[:12].tolist()}

        return m 

    # ===================================================
    # SAVE FUNCTIONS
    # ===================================================

    def save(self, buf):
        """
        Method to serialize buffer based on protocol

        """
        _, meta = unpack_meta(buf)
        protocol, fname = meta['fname'].split('://')

        if protocol in self.SAVE_FUNCS:
            self.SAVE_FUNCS[protocol](buf, fname)

        return fname

    def save_redis(self, buf, fname):

        self.rc.set_buf(fname, buf)

    def save_local(self, buf, fname):

        arr, meta = unpack(buf)

        # --- Apply func_defs
        if 'saved' in meta:

            fdefs = meta['saved'].get('fdefs', None)

            if fdefs is not None:

                # --- Create fnames, kwargs, sid
                fdefs = funcs.init(fdefs)
                sid = meta['saved']['sid']

                db = DB(meta['saved']['fname'])
                db.apply_row(sid=sid, fdefs=fdefs, fnames={'$arr': arr}, replace=True)
                db.to_csv()

        # --- Parse kwargs
        kwargs = {}
        if 'coord' in meta:
            kwargs = {'meta': {'affine': meta['coord']['affine']}}

        # --- Save
        io.save(fname, arr, **kwargs)
