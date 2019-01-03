#!/usr/bin/env python
# -*- coding:utf-8 -*

import os,sys,time
from fisync import *


if __name__=='__main__':
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)
    except OSError, e:
        print >>sys.stderr, 'fork failed: %d (%s)' % (e.errno, e.strerror)
        sys.exit(1)
    os.setsid()
    os.umask(0)
    print('Start Runing...')
    
    while True:
        initRedis()
        #diffRedis()
        time.sleep(3600)




