# Tencent CDN Missing MD5 Header

## Summary

From 2026-06-08 through at least 2026-06-11, the scheduled `track` workflow repeatedly detected a new WeChat installer but failed while preparing release metadata.

The affected public download URL was:

```text
https://dldir1v6.qq.com/weixin/Universal/Windows/WeChatWin_4.1.10.exe
```

## Observed Behavior

The workflow logs showed that `scripts/check-update.py` found the installer URL, extracted public version `4.1.10`, and read this release timestamp from `Last-Modified`:

```text
Mon, 08 Jun 2026 02:03:43 GMT
```

The installer download completed, and `scripts/do-update.py` computed this local MD5:

```text
05c09e4ecc74ef85f036c05f2f69e6ca
```

However, the workflow's HEAD response did not provide the expected `X-COS-META-MD5` header, so the script compared the computed hash with `<unknown>` and returned missing metadata:

```text
Hash mismatch! Expected: <unknown>, Got: 05c09e4ecc74ef85f036c05f2f69e6ca
TypeError: float() argument must be a string or a real number, not 'NoneType'
```

The crash happened when release note generation tried to format a missing size value.

## Later Recheck

A later HEAD-only recheck from a different environment returned the expected metadata:

```text
X-COS-META-MD5: 05c09e4ecc74ef85f036c05f2f69e6ca
Content-Length: 239404080
Last-Modified: Mon, 08 Jun 2026 02:03:43 GMT
```

This suggests Tencent CDN metadata headers can vary by time, edge, or request path. The `X-COS-META-MD5` header is useful when present, but should not be treated as guaranteed.

## Tracker Policy

When server metadata is present, validate the downloaded installer against it.

When optional server metadata is missing, continue with locally computed metadata and add a warning to generated release notes.
