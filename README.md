
#升级引擎工具A篇

##适用范围
对引擎源码没有修改或扩展的cocos2d-x/cocos2d-js项目，或者只做过少量修改。否则请查看`升级引擎工具B篇。`

##准备工作
#####1 保证git能正常运行

#####2 以下内容加入~/.bash_profile
	export LC_CTYPE=C 
	export LANG=C

#####3 安装wiggle
	$ sudo apt-get install -y wiggle
	or
	$ brew install -y wiggle

##如何使用

有两种升级方式，请按自己的情况选择。

第一种方式，会根据游戏工程的引擎版本自动寻找下载对应的升级文件。

第二种方式，你需要自行指定升级文件，不过你可以自己创建符合自己需求的升级文件，请查看`制作升级文件`。

	$ python cocos_upgrade.py -d /Users/testUpgrade -n testUpgrade -v 3.5
	
-d 游戏工程目录，请使用工程全路径。

-n 游戏工程名称，请注意工程名有时与目录名称不一致，建议参考xcode工程名。

-v 要升级的引擎版本，请查看`支持的版本`。

	$ python cocos_upgrade2.py -d /Users/testUpgrade -n testUpgrade -p /Users/test30-35.diff

-d 游戏工程目录，请使用工程全路径。

-n 游戏工程名称，请注意工程名有时与目录名称不一致，建议参考xcode工程名。

-p 升级用补丁，升级用补丁的文件全路径。此文件可到[cocos官方网站下载](http://www.cocos2d-x.org)下载，也可以自行制作。



##支持的版本

目前只支持从低版本升级到高版本，版本在以下范围内才能升级。

	Cocos2d-x(C++/Lua): 3.0 3.1 3.2 3.3 3.4 3.5
	Cocos2d-Js: 3.0 3.1 3.2 3.3 3.5
	
	
##升级说明
升级工具会自动更新引擎源码，工程配置(.pbproj/.mk/.sln）文件，同时会产生少量文件冲突。

请解决冲突后编译运行。


##制作升级文件
例如，你的游戏工程是基于Cocos2d-x 3.2
开发，希望升级到3.5，那么你需要用3.2创建A工程，再用3.5创建另外一个B工程，我们提供了一个工具帮助你制作属于自己的补丁。生成的文件A-B.diff在当前目录下。

	$ python cocos_make_patch.py -s A -d B

-s 要升级的工程，请使用工程全路径。

-d 升级目标工程，请使用工程全路径。

最后调用cocos_upgrade2.py来调用补丁进行升级。
