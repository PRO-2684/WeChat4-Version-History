# WeChat4-Version-History

[English](README.md) | 简体中文 | ![GitHub Release](https://img.shields.io/github/v/release/PRO-2684/WeChat4-Version-History?logo=wechat&color=07c160)

此仓库自动跟踪 [微信 4.0.0](https://pc.weixin.qq.com/) 自从 `4.0.0.35` (2024-11-20) 以来的公开版本历史。

## [`versions.json`](versions.json)

此文件包含微信 4 自从 `4.0.0.35` 以来的版本历史。其结构如下：

```json
[
    {
        "released": "<release date in ISO8601>",
        "size": <installer size in bytes>,
        "md5": "<installer MD5>",
        "version": "<version number>",
    },
    ...
]
```

## 相关项目

- [QQNT-Version-History](https://github.com/PRO-2684/qqnt-version-history): 自动跟踪 [QQNT](https://im.qq.com/pcqq/index.shtml) 的版本历史。
- [wechat-windows-versions](https://github.com/tom-snow/wechat-windows-versions): 自动跟踪 [微信 3](https://pc.weixin.qq.com/) 的版本历史。
