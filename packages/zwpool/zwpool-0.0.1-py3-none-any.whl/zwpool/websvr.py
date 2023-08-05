import os
import json
import time, threading
import web
from cheroot.server import HTTPServer
from cheroot.ssl.builtin import BuiltinSSLAdapter

from zwpool.__version__ import __version__
from zwutils.config import Config
from zwpool.proxy.proxypool import ProxyPool

from zwutils.logger import logger
LOG = logger(__name__)

class Base:
    def __init__(self):
        web.header('Content-Type', 'application/json;charset=utf-8')
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Methods', 'GET, POST')
        web.header('Access-Control-Allow-Credentials', 'true')

URLS = (
    '/', 'index',
    '/(js|css|images)/(.*)', 'static',
    '/proxy/status', 'ProxyStatus',
    '/proxy/get', 'ProxyGet',
)
HTML = web.template.render('html')
PROXY_POOL_CFG = Config('conf/proxypool.json')
PROXY_POOL = ProxyPool(PROXY_POOL_CFG)

class static(Base):
    def GET(self, media, file):
        try:
            f = open('html/'+media+'/'+file, 'rb')
            return f.read()
        except:
            return ''

class docs:
    def GET(self):
        return HTML.docs()

class ProxyStatus(Base):
    def POST(self):
        rtn = PROXY_POOL.status()
        return json.dumps(rtn)
    def GET(self):
        return self.POST()

class ProxyGet(Base):
    def POST(self):
        rtn = PROXY_POOL.random_proxy()
        return json.dumps(rtn)
    def GET(self):
        return self.POST()

def run_task():
    LOG.info('Fetch and test proxy start.')
    PROXY_POOL.fetch_proxy()
    PROXY_POOL.test_proxy()
    threading.Timer(PROXY_POOL_CFG.fetch_frq, run_task).start()
    LOG.info('Fetch and test proxy finish.')

class MyApplication(web.application):
    def run(self, port, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

def run_websvr():
    defcfg = {
        'listen_port': 13603,
        'enable_https': False,
    }
    cfg = Config('conf/poolsvr.json', default=defcfg)
    port = cfg.listen_port or defcfg['listen_port']
    enable_https = cfg.enable_https or defcfg['enable_https']
    LOG.info('*'*80)
    LOG.info('Version: %s', __version__)
    LOG.info('Port: %s', port)
    LOG.info('Https enable: %s', enable_https)
    LOG.info('*'*80)

    run_task()
    if enable_https:
        HTTPServer.ssl_adapter = BuiltinSSLAdapter(
            certificate='conf/server.crt',
            private_key='conf/server.key')
    app = MyApplication(URLS, globals())
    app.run(port=port)
