## 使用方法
### 有python运行环境
```
git clone https://github.com/azusemst/bili-danmu-reader.git
python reader.py [-m FILEPATH] [-d FILEPATH] [-b] [-g or --gift]
```
### 使用exe
1. 下载最新的[Release](https://github.com/azusemst/bili-danmu-reader/releases)
2. 把从 [matsuri.icu](https://matsuri.icu/) 或者 [danmakus.com](https://danmakus.com/search) 下载的直播弹幕`.json`文件放在同一文件夹下
3. 双击运行`reader.exe`，或者使用命令行：
```
./reader.exe [-m FILEPATH] [-d FILEPATH] [-b] [-g or --gift]
```

## CLI arguments
如果不加arguments则自动打开最新的弹幕文件
### -m FILEPATH
指定特定的从matsuri上下载的文件
### -d FILEPATH
指定特定的从danmakus上下载的文件
### -b
不打开浏览器
### -g --gift
跳过礼物