
#升级引擎工具B篇

##适用范围
所有cocos2d-x/cocos2d-js项目。用此工具升级，需开发者自行对比升级后的差异。自动升级请查看[升级引擎工具A篇。](https://github.com/calfjohn/cocosUpgrade/blob/SemiAutomatic/README.md)

##准备工作
#####1 下载安装

[点击下载Diffmerge](https://sourcegear.com/diffmerge/downloads.php)，这是一个免费软件。

#####2 配置Diffmerge命令行
	$ sudo cp /Applications/DiffMerge.app/Contents/Resources/diffmerge.sh /usr/bin
	$ diffmerge.sh
	
#####3 安装python
	$ python --version 
	Python 2.7.6

#####4 下载原引擎版本和目标引擎版本
比如你的游戏基于cocos2d-x 3.2，希望升级到cocos2d-x 3.5，那就下载3.2和3.5。

[请到这里下载。](http://www.cocos2d-x.org/download/version)

##如何使用

	$ python cocos_upgrade.py -s /Users/cocos2d-x-3.2 -d /Users/cocos2d-x-3.5 -p /Users/testProject

-s 原引擎目录，请使用全路径。

-d 目标引擎目录，请使用全路径。

-p 待升级的工程目录，请使用全路径。

`特别提醒：升级工作是在游戏工程的副本上进行的，副本目录是/Users/testProjectUpgrade/target／testProject`

##支持的版本

目前只支持从低版本升级到高版本，版本在以下范围内才能升级。

	Cocos2d-x(C++/Lua): 3.0 3.1 3.2 3.3 3.4 3.5
	Cocos2d-Js: 3.0 3.1 3.2 3.3 3.5	
	
##升级说明
#####1 升级工具会替换引擎目录，修改游戏工程配置(.pbproj/.mk/.sln等）文件

#####2 自动记录游戏工程中引擎相关修改，并通过Diffmerge工具对修改内容进行对比，帮助开发者合并代码。

#####3 Diffmerge窗口内有三个打开的文件界面，左边是你的游戏工程文件，右边是引擎HelloWorld工程文件（即默认初始代码），中间是升级后的游戏工程文件，我们分别称为L文件、R文件和C文件。


只要三个文件中有任意两个内容不一致，Diffmerge就会用颜色标记出来，一般我们只需要处理界面最左边竖条内标记为`红色`的部分－－－那表示L与R不一致，同时L与C也不一样，这些就是开发者在原来引擎基础上修改的代码。开发者需要判断L文件中的内容，如何合并到C文件中。
![Mou icon](https://github.com/calfjohn/cocosUpgrade/blob/SemiAutomatic/images/Compare3files.jpeg?raw=true)


#####4 Diffmerge有一些异常情况如下：

这种表示二进制文件不同，这种情况不用关注，直接关闭退出Diffmerge。
![Mou icon](https://github.com/calfjohn/cocosUpgrade/blob/SemiAutomatic/images/BinaryCompare.jpg?raw=true)


这种表示在升级后的工程内，这个文件不存在了，开发者需要判断是否需要手动把这个文件从游戏工程中拷贝到升级后的工程内。处理完成后关闭这个提示。

![Mou icon](https://github.com/calfjohn/cocosUpgrade/blob/SemiAutomatic/images/NotFoundFile.jpg?raw=true)

