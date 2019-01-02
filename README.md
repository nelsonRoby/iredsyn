# redino

一个redis与inotify组合下的工具，设想将需要同步的文件写进redis里，然后将它同步到所有需要的地方，那怕是100G也无所谓,因为我们关注是当前需要更新的文件。

	#全局变量
	[global]
	#REDIS主机
	rdhost = 127.0.0.1
	#redis端口
	rdport = 6379
	#redis 密码
	rdpass = 123

	#rsync目标1
	[sydst1]
	#rsync主机
	host = 1.1.1.1
	#rsync用户名
	user = file
	#rsync密码文件
	pwdf = aaa.pwd
	#rsync目标名
	tnae = bakfile
	mode = 1 (1为正常模式，2为本地挂载)
	#rsync目录（限本地挂载方式生效）
	tdir = /tmp/aaa/

