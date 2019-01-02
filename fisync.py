#!/usr/bin/python
# -*- coding:utf-8 -*

import os
from frconf import *
from fredis import *

# pool0 = redis.ConnectionPool(host=rdhost,port=rdport,db=0)
# r0 = redis.Redis(connection_pool=pool0)
# k0 = r0.keys()
# pool2 = redis.ConnectionPool(host=rdhost,port=rdport,db=1)
# r2 = redis.Redis(connection_pool=pool2)

r0 = conRedis(host=rdhost,port=rdport,id=0,pwd=rdpass)
k0 = r0.keys()
r1 = conRedis(host=rdhost,port=rdport,id=1,pwd=rdpass)

# get file attribute to redis
def initRedis():
    if not testInit():
        fcount = 0
        for p,dirs,fs in os.walk(fpath):
            for f in fs:
                file = os.path.join(p,f)
                # if f.endswith('00.jpg'):
                #     print(f)
                #     fwRedis(file)
                fwRedis(file)
                fcount += 1
        updatetime = int(time.time())
        node = "node-%s" %fstag
        shKey(node,{"updatetime":updatetime,"filenum":fcount})
    else:
        cmd = "find %s -type f -mtime 0" %fpath
        data = os.popen(cmd).read().split('\n')
        for d in data:
            if d :
                n = d.split('/')[-1]
                k = fgMd5(n,'s')
                info = ghKey(k)
                if info:
                    oldhash=info['filehash']
                    updatetime = int(time.time())
                    filetag = fstag
                    shKey(k,{"updatetime":updatetime,"oldhash":oldhash,"filetag":filetag})
                else:
                    fwRedis(d)
            else:
                pass

#syn the local file to remote
def synfile(n,file):
    cmd = ""
    num = n.split('-')[1]
    mode = int(config.get(n,"symode"))
    if mode == 2:
        cmd = "/usr/bin/cp -fr %s %s " %(file,config.get(n,"sydisk"))
    elif mode == 1:
        host = "%s@%s::%s" %(config.get(n,"syuser"),config.get(n,"dthost"),config.get(n,"syname"))
        cmd = "rsync -avz %s %s" %(file,host)
    print(cmd)

# the redis keys difference between local and remote
def diffRedis():
    for n in nodes:
        if n == "global":
            continue
        rshost=config.get(n,'dthost')
        rsport=config.get(n,'rdport')
        rspass=config.get(n,'rdpass')
        # pool = redis.ConnectionPool(host=rshost, port=rsport)
        # rt = redis.Redis(connection_pool=pool)
        # k1 = rt.keys()
        # data = list(set(k0).difference(set(k1)))
        rt = conRedis(host=rshost, port=rsport,pwd=rspass)
        if rt:
            kt = rt.keys()
            data = set(k0) - set(kt)

            #avoid to sync the larger number files.
            if len(data) >100000:
                break
            for d in data:
                if d not in r1.keys():
                    fd = ghKey(d)
                    fn = fd['filename']
                    r1.hmset(d, fd)
                    r1.expire(d, 3600 * 24)
                    synfile(n, fn)
        else:
            continue

def inotRedis(file):
    if not file.startswith('sh-thd'):
        data = fgAttr(file)
        filetag = fstag
        data[1].update({"filetag":filetag})
        shKey(data[0], data[1])

