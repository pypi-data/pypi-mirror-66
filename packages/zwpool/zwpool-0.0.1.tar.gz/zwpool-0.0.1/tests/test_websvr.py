# -*- coding: utf-8 -*-
import pytest
import os
import sys
TEST_DIR = os.path.abspath(os.path.dirname(__file__))
PARENT_DIR = os.path.join(TEST_DIR, '..')
sys.path.insert(0, PARENT_DIR)

from zwpool.websvr import run_websvr

if __name__ == '__main__':
    run_websvr()