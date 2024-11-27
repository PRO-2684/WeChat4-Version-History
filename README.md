# WeChat4-Version-History

English | [简体中文](README.zh-CN.md)

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/PRO-2684/wechat4-version-history/Update%20Versions?label=Update%20Versions&logo=github)](

This repo automatically tracks public version history of [WeChat 4.0.0](https://pc.weixin.qq.com/), since `4.0.0.35` (2024-11-20).

## [`versions.json`](versions.json)

This file contains the version history of WeChat4 since `4.0.0.35`. It is structured as follows:

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

## Related Projects

- [QQNT-Version-History](https://github.com/PRO-2684/qqnt-version-history): Automatically tracks version history of [QQNT](https://im.qq.com/pcqq/index.shtml).
- [wechat-windows-versions](https://github.com/tom-snow/wechat-windows-versions): Automatically tracks version history of [WeChat3](https://pc.weixin.qq.com/).
