from requests import Session
from os import environ
from json import load
from dateutil.parser import parse

URL = "https://dldir1v6.qq.com/weixin/Universal/Windows/WeChatWin.exe"
x = Session()

def setOutput(key, value):
    """Set the output for GitHub Actions."""
    if "GITHUB_OUTPUT" in environ:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")


def lastModified(url):
    """Get the last modified date of the file at the specified URL."""
    r = x.head(url)
    date = r.headers.get("Last-Modified")
    # e.g. Wed, 20 Nov 2024 06:20:18 GMT
    return parse(date)


def main():
    releasedNow = lastModified(URL)
    with open("versions.json", "r") as f:
        data = load(f)
    releasedBefore = data[-1]["released"] if data else "1970-01-01T00:00:00+00:00"
    releasedBefore = parse(releasedBefore)
    if releasedNow > releasedBefore:
        setOutput("released", releasedNow.isoformat())
        setOutput("url", URL)
    else:
        setOutput("released", "none")

    # Output be like:
    # released=2024-11-20T06:20:18+00:00
    # url=https://dldir1v6.qq.com/weixin/Universal/Windows/WeChatWin.exe

if __name__ == "__main__":
    main()
