# 网易云HA插件

Fork from https://github.com/shaonianzhentan/ha_cloud_music

## 修改内容

> 已针对Chromecast的Google Home/Nest/TV 设备播放修复功能并优化

> 保持原有Repo中所有功能

## 详细
设置时支持所有播放器，其中例如VLC等部分播放器中代码参数没有文档没有提取

![设置时支持所有播放器](images/WX20220325-140124@2x.png)

支持Chromecast等HA中Media Player选择

![支持Chromecast等HA中Media Player选择](images/WX20220325-140137@2x.png)

当选择Chromecast作为播放器时，增加音乐元信息推送，显示在HA中及带屏幕的Google设备

![增加Chromecast播放器音乐元信息推送，支持显示在HA中及Google设备上](images/screenshot_media_player.png)

## TODO

- [ ] 顺序、随机、循环播放修复
- [ ] Google Home语音控制