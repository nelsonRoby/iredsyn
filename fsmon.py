#!/usr/bin/env python
# -*- coding:utf-8 -*

import os,time,sys
import subprocess
from  pyinotify import  WatchManager, Notifier,ProcessEvent,IN_DELETE,IN_CREATE,IN_MODIFY,IN_CLOSE_WRITE
from fisync import *
		
class EventHandler(ProcessEvent):
    """Handle"""
    def process_IN_CLOSE_WRITE(self, event):
        if event.name.startswith('.') or event.name.endswith('~') or event.name=='4913':
            pass
        else:
            inotRedis(str(event.pathname))
			
    def process_IN_DELETE(self, event):
        if event.name.startswith('.') or event.name.endswith('~') or event.name=='4913':
            pass
        else:
            print(event.pathname)
			
def FSMonitor(path='/tmp'):
        wm = WatchManager()
        mask = IN_DELETE | IN_CLOSE_WRITE | IN_CREATE
        notifier = Notifier(wm, EventHandler(),read_freq=10)
        notifier.coalesce_events()
        # 设置受监视的事件，这里只监视文件创建事件，（rec=True, auto_add=True）为递归处理
        wm.add_watch(path,mask,rec=True, auto_add=True)
        notifier.loop()
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
    FSMonitor('/tmp')
    print 'Start Runing....'