from requests import Session
from os import environ
from json import load
from dateutil.parser import parse
from bs4 import BeautifulSoup
from typing import Optional
from re import compile


URL = "https://pc.weixin.qq.com/"
VERSION_REGEX = compile(r'WeChatWin_(\d+\.\d+\.\d+)\.exe')

x = Session()

def get_download_url() -> Optional[str]:
    """Get the download URL from the WeChat PC download page."""
    r = x.get(URL)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'html.parser')
    # <a class="download-button" id="downloadButton" href="https://dldir1v6.qq.com/weixin/Universal/Windows/WeChatWin_4.1.6.exe" role="button">
    download_button = soup.find('a', {'id': 'downloadButton'})
    if download_button:
        href = download_button.get('href')
        print(f"[get_download_url] Found download URL: {href}")
        return href
    else:
        print("[get_download_url] Download button not found.")
        return None


def version_from_url(url: str) -> Optional[str]:
    """Extract the version number from the download URL."""
    match = VERSION_REGEX.search(url)
    if match:
        print(f"[version_from_url] Extracted version: {match.group(1)}")
        return match.group(1)
    else:
        print("[version_from_url] No version found in URL.")
        return None


def set_output(key: str, value: str):
    """Set the output for GitHub Actions if in a GitHub Actions environment. Also print to stdout for debugging."""
    if "GITHUB_OUTPUT" in environ:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")


def last_modified(url: str):
    """Get the last modified date of the file at the specified URL."""
    r = x.head(url)
    date = r.headers.get("Last-Modified")
    # e.g. Wed, 20 Nov 2024 06:20:18 GMT
    print(f"[last_modified] Last-Modified header: {date}")
    return parse(date)


def main():
    download_url = get_download_url()
    if not download_url:
        raise RuntimeError("Could not find download URL")

    version = version_from_url(download_url)
    release_date = last_modified(download_url)
    with open("versions.json", "r") as f:
        data = load(f)
    released_before = data[-1]["released"] if data else "1970-01-01T00:00:00+00:00"
    released_before = parse(released_before)
    if release_date > released_before:
        print(f"[main] New version found: {version} released on {release_date.isoformat()}")
        set_output("released", release_date.isoformat())
        set_output("url", download_url)
    else:
        print("[main] No new version found.")
        set_output("released", "none")

    # Output be like:
    # released=2025-12-18T04:26:28+00:00
    # url=https://dldir1v6.qq.com/weixin/Universal/Windows/WeChatWin_4.1.6.exe


if __name__ == "__main__":
    main()
