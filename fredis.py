#!/usr/bin/python
# -*- coding:utf-8 -*

import os,time
import redis
import hashlib
import re

from frconf import *

def conRedis(host,port,id=0,pwd=''):
    try:
        if pwd == '':
            pool = redis.ConnectionPool(host=host, port=port,db=id)
        else:
            pool = redis.ConnectionPool(host=host, port=port, db=id, password=pwd)
        rp = redis.Redis(connection_pool=pool)
        rp.get('abc')
        return rp
    except redis.ConnectionError:
        print("Error!")
        return 0
    else:
        print("no!")
        return 0

# pool = redis.ConnectionPool(host=rdhost,port=rdport,db=0)
# r0 = redis.Redis(connection_pool=pool)
r0 = conRedis(host=rdhost,port=rdport,id=0,pwd=rdpass)

#get the file or filename md5
def fgMd5(str,type="f"):
    md5obj = hashlib.md5()
    if type == "f":
        f = open(str, 'rb')
        md5obj.update(f.read())
    elif type == "s":
        md5obj.update(str)
    else:
        return None
    hash = md5obj.hexdigest()
    return hash

# Get the file attribute
def fgAttr(file):
    data = []
    fm=fgMd5(file.split('/')[-1],"s")
    data.append(fm)
    createtime = os.path.getctime(file)
    filesize = os.path.getsize(file)
    updatetime = int(time.time())

    filehash = fgMd5(file, "f")
    file_dict = {"filename": file, "filesize": filesize,"filehash":filehash, "createtime": createtime, "updatetime": updatetime}
    data.append(file_dict)
    return data

#write file hash in the redis
def fwRedis(file):
    data = fgAttr(file)
    r0.hmset(data[0],data[1])

#get all redis hash keys
def fgRedis():
    hdata = {}
    for k in r0.keys():
        if len(k) == 32:
            hdata[k] = r0.hgetall(k)
    return hdata

#get the hash key
def ghKey(k):
    data = r0.hgetall(k)
    return data

#set the hash key
def shKey(k,data):
    r0.hmset(k,data)

# check the system if init.
def testInit():
    node = "node-%s" %(fstag)
    data = ghKey(node)
    if data :
        return 1
    else:
        keys = r0.keys()
        count = 0
        for k in keys:
            if len(k) == 32:
                count += 1
        if count > 10000:
            updatetime = int(time.time())
            shKey(node, {"updatetime": updatetime, "filenum": count})
        else:
            return 0


