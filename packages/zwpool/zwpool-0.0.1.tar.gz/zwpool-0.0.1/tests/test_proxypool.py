# -*- coding: utf-8 -*-
import pytest
import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from zwutils.config import Config
from zwpool.proxy.proxypool import ProxyPool
from zwutils import logger
LOG = logger.logger(__name__, cfg='conf/log.json')

if __name__ == '__main__':
    cfg = Config('conf/proxypool.json', default={'db':'redis://:pwd@host:port/0'})
    pp = ProxyPool(cfg)
    # pp.fetch_proxy()
    # proxy = pp.random_proxy()
    # pp.test_proxy()
