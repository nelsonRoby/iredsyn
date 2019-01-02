# iredsync

一个redis与inotify组合下的工具，将需要同步的文件写进redis里，然后将它同步到所有需要的地方。
主要针对数量众多小文件，以及历史架构造成的问题。
	
### 原理：参考硬件阵列当中的RAID5思想。

### 全局变量
	[global]
	#REDIS主机
	rdhost = 127.0.0.1
	#redis端口
	rdport = 6379
	#redis 密码
	rdpass = 123
	sypath = /data
	srctag = test
	inloop = 0
	debug = 0
	
### rsync目标1
	[sydst-1]
	#rsync主机
	dthost = 1.1.1.1
	#rsync用户名
	syuser = file
	#rsync密码文件
	sypwdf = aaa.pwd
	#rsync目标名
	syname = bakfile
	#1为正常模式，2为本地挂载
	symode = 1
	#rsync目录（限本地挂载方式生效）
	sydisk = /tmp/aaa/
	rdport = 6379
	rdpass = 123

