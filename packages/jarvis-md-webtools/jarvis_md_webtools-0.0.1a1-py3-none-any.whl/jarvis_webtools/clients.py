import os, requests
import numpy as np
import hashlib, base64
import redis
from .npack import *

class BaseClient():

    def __init__(self, host='localhost', port=7787, sock='/mnt/tmp/redis.sock', prefix='JARVIS_REDIS'):

        self.configs = {
            'host': host,
            'port': port,
            'sock': sock}

        # --- Get default environment variables if defined
        self.check_environ_configs(prefix)

        # --- Initialize client
        self.init_client()

    def init_client(self): pass

    def check_environ_configs(self, prefix='JARVIS_REDIS'):
        """
        Method to check entries in self.configs for preset environmental var 

        """
        for k in self.configs:
            k_ = (prefix+ '_' + k).upper()
            if k_ in os.environ:
                self.configs[k] = int(os.environ[k_]) if os.environ[k_].isnumeric() else os.environ[k_]

class RedisClient(BaseClient):

    def init_client(self):

        # --- Initialize random client user 
        self.init_user_id()

        # --- Initialize client (TCP/IP vs. SOCKETS)
        if self.configs['host'] is not None:
            self.redis = redis.StrictRedis(host=self.configs['host'], port=self.configs['port'])

        else:
            self.redis = redis.StrictRedis(unix_socket_path=self.configs['sock'])

    def init_user_id(self):
        """
        Method to generate unique username by combining HOME address + MAC address

        """
        self.user = self.sha1(bytes(os.environ['HOME'], 'utf-8')) 

    def set_buf(self, h, buf):
        """
        Method to set packed buffer in database

        """
        self.redis.set(h, buf)

    def set_buf_raw(self, buf):
        """
        Method to set packed buffer in database WITHOUT h

        """
        size, meta = unpack_meta(buf)
        h = meta['fname'][8:]
        self.redis.set(h, buf)

        return h

    def set_arr_meta(self, h, arr, meta):
        """
        Method to set Numpy arr + JSON meta in database

        :params

          (str) h : hash filename 

        """
        self.redis.set(h, pack(arr, meta))

    def get_buf(self, h, delete=True):
        """
        Method to get data from database

        """
        buf = self.redis.get(h)

        if delete:
            self.redis.delete(h)

        return buf 

    def get_arr_meta(self, h, delete=True):
        """
        Method to get data from database and convert to Numpy array

        """
        buf = self.get_buf(h, delete=delete)
        arr, meta = unpack(buf) 
        
        return arr, meta 

    def random_hash(self):

        return self.sha1(np.random.rand(1).tobytes())

    def sha1(self, b, length=8):

        m = hashlib.sha1()
        m.update(b)

        return base64.urlsafe_b64encode(m.digest()).decode('ascii')[:length]

    def send_arrs(self, arrs, vsize=[1, 1, 1]):
        """
        Method to send arrs to Redis database

        """
        fnames = {}

        for key, arr in arrs.items():

            if type(arr) is np.ndarray:

                h = self.random_hash()
                fname = 'redis://%s' % h
                self.set_arr_meta(h, arr, {'fname': fname, 'vsize': vsize})

            if type(arr) is str:

                fname = 'local://%s' % arr

            fnames[key] = fname

        return fnames 

    def clear(self):
        """
        Method to clear db 

        """
        self.redis.flushdb()

class FlaskClient(BaseClient):

    def post(self, meta):
        """
        Method to send metadata JSON object

        """
        URL = 'http://%s:%s/show' % (self.configs['host'], self.configs['port'])
        requests.post(URL, json=meta)
