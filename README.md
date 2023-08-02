## 使用方法
### 有python运行环境
```
git clone https://github.com/azusemst/bili-danmu-reader.git
python reader.py [-m FILEPATH] [-d FILEPATH] [-b] [-g or --gift]
```
### 使用exe
1. 下载最新的[Release](https://github.com/azusemst/bili-danmu-reader/releases)
2. 把从 [matsuri.icu](https://matsuri.icu/) 或者 [danmakus.com](https://danmakus.com/search) [下载](#下载弹幕文件的方法)的直播弹幕`.json`文件放在同一文件夹下
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

## 下载弹幕文件的方法
### [matsuri.icu](https://matsuri.icu/)
1. 搜索[主播](https://matsuri.icu/channel/3035105)
2. 选择[直播场次](https://matsuri.icu/detail/N3gJAhM1rpEjXQ)
3. 点击显示所有弹幕
4. 下载JSON
![image](https://github.com/azusemst/bili-danmu-reader/assets/50971762/8c0c638d-96d6-4c33-acf9-9e695ed3aee8)

### [danmakus.com](https://danmakus.com/search)
1. 搜索[主播](https://danmakus.com/channel/3035105)
2. 选择[直播场次](https://danmakus.com/live/ff91f0d9-e126-4bb6-91a0-6ce6fde04c17)
3. 打开弹幕工具，选择导出，选择JSON
![image](https://github.com/azusemst/bili-danmu-reader/assets/50971762/66854867-e6ca-4f09-a505-f04df2cdfb6a)
