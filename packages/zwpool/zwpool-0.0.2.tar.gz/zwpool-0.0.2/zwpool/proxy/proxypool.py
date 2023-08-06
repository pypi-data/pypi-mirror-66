import re
import time
import requests
import inspect
import random

from zwpool.proxy import freeproxy
from zwdb.zwredis import ZWRedis
from zwutils.mthreading import multithread_task
from zwutils.config import Config

class ProxyPool(object):
    def __init__(self, cfg):
        self.cfg = cfg or Config('conf/proxypool.json', default={
            'db':'redis://:pwd@host:port/0',
            'fetch_frq': 60,
        })
        self.db = ZWRedis(cfg.db)
        self.thread_num = 10 # thread num cfg for multithread_task
        self.timeout_fetch = 10
        self.timeout_random = 5
        self.retry_random_num = 5
    
    def close(self):
        self.db.close()
    
    def freeproxy_funcs(self):
        funcs = inspect.getmembers(freeproxy.FreeProxy, predicate=inspect.isfunction)
        return funcs
    
    def valid_proxy(self, proxy, site=None, timeout=None):
        succ = False
        tout = timeout or self.timeout_fetch
        try:
            r = requests.get('http://www.baidu.com', proxies=proxy, timeout=tout, verify=False)
            if r.status_code == 200:
                succ = True
        except Exception:
            pass
        t = 'http' if 'http' in proxy else 'https'
        return {
            'succ'  : succ,
            'type'  : t,
            'proxy' : proxy[t],
            'site'  : site,
            'ts'    : str(time.time()),
        }
    
    def fetch_proxy(self):
        funcs = self.freeproxy_funcs()
        proxies = []
        for func in funcs:
            for proxy in func[1]():
                s = {'proxy': {'https' if proxy.startswith('https') else 'http': proxy}, 'site':func[0]}
                proxies.append(s)

        results = multithread_task(self.valid_proxy, proxies, settings=self)
        for r in results:
            rt = r.result
            if rt['succ']:
                del rt['succ']
                self.db.set(rt['proxy'], rt)
    
    def test_proxy(self):
        proxies = self.db.all()
        for proxy in proxies:
            key = proxy['key']
            proxy = proxy['value']
            if 'proxy' not in proxy:
                self.db.delete(key)
                continue
            proxy = {proxy['type']: proxy['proxy']}

            url_re = r'[a-zA-z]+://[^\s]*'
            _a = re.findall(url_re, key)
            if len(_a)>0:
                r = self.valid_proxy(proxy)
                if not r['succ']:
                    self.db.delete(key)
            else:
                self.db.delete(key)

    def random_proxy(self):
        count = self.retry_random_num
        valid = False
        while count>0 and not valid:
            p = self._random_proxy()
            valid = self.valid_proxy(p, timeout=self.timeout_random)
            count -= 1
        return p if valid else None
    
    def _random_proxy(self):
        key = self.db.conn.randomkey()
        if not key:
            return None
        proxy = self.db.get(key)
        proxy = {proxy['type']: proxy['proxy']}
        return proxy
    
    def status(self):
        funcs = self.freeproxy_funcs()
        funcs = [f[0] for f in funcs]
        rtn = {
            'total': self.db.dbsize(),
            'sources': ','.join(funcs)
        }
        return rtn
        
        



    
