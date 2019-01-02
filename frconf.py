#!/usr/bin/python
# -*- coding:utf-8 -*

import os,time
import ConfigParser

config = ConfigParser.ConfigParser()
local_path = os.path.abspath(os.path.join(os.path.dirname(__file__)))
config_ini = local_path + "/config.ini"
config.read(config_ini)
nodes = config.sections()

rdhost = config.get("global","rdhost")
rdport = config.get("global","rdport")
rdpass = config.get("global","rdpass")

fstag = config.get("global","srctag")
floop = config.get("global","inloop")
fpath = config.get("global","sypath")
