
#升级引擎工具B篇

##适用范围
所有cocos2d-x/cocos2d-js项目。用此工具升级，需开发者自行对比升级后的差异。自动升级请查看`升级引擎工具A篇。`

##准备工作
#####1 保证git能正常运行

#####2 下载安装[Diffmerge](https://sourcegear.com/diffmerge/downloads.php)

#####3 配置Diffmerge命令行
	$ sudo cp /Applications/DiffMerge.app/Contents/Resources/diffmerge.sh /usr/bin
#####4 安装python

#####5 下载原引擎版本和目标引擎版本
如果你的游戏基于cocos2d-x 3.2，希望升级到cocos2d-x 3.5，[请到这里下载。](http://www.cocos2d-x.org/download/version)


##如何使用

	$ python cocos_upgrade.py -s /Users/cocos2d-x-3.2 -d /Users/cocos2d-x-3.5 -p /Users/testUpgrade

-s 原引擎目录，请使用全路径。

-d 目标引擎目录，请使用全路径。

-p 待升级的工程目录，请使用全路径。


##支持的版本

目前只支持从低版本升级到高版本，版本在以下范围内才能升级。

	Cocos2d-x(C++/Lua): 3.0 3.1 3.2 3.3 3.4 3.5
	Cocos2d-Js: 3.0 3.1 3.2 3.3 3.5	
	
##升级说明
升级工具会替换引擎源码，引擎工程配置(.pbproj/.mk/.sln）文件，自动记录开发者对引擎的修改，并通过调用Diffmerge工具对修改进行对比，帮助开发者合并代码。