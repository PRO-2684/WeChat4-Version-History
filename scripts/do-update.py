from requests import Session
from json import load, dump
from subprocess import check_output
from os import environ
from os.path import getsize
from hashlib import md5
from argparse import ArgumentParser
from humanize import naturalsize
from re import search

x = Session()
parser = ArgumentParser()
# Accept 2 arguments: `released` and `url`
parser.add_argument("--released", type=str, help="The date and time of the release.")
parser.add_argument("--url", type=str, help="The URL of the installation package.")
args = parser.parse_args()
newData = {
    "released": args.released,
    "size": -1,
    "md5": "<unknown>",
    "version": "<unknown>",
}


def setOutput(key, value):
    """Set the output for GitHub Actions."""
    if "GITHUB_OUTPUT" in environ:
        with open(environ["GITHUB_OUTPUT"], "a") as f:
            f.write(f"{key}={value}\n")
    print(f"{key}={value}")


def getStat(url, file, directory="./downloads"):
    """Get and validate the stat of the file at the specified URL."""
    r = x.head(url)
    # Using `X-COS-META-MD5` header
    expectedHash = r.headers.get("X-COS-META-MD5") or "<unknown>"
    # Calculate MD5 hash of the file
    path = f"{directory}/{file}"
    with open(path, "rb") as f:  # https://stackoverflow.com/a/59056837/16468609
        hash = md5()
        while chunk := f.read(8192):
            hash.update(chunk)
    actualHash = hash.hexdigest()
    expectedSize = int(r.headers.get("Content-Length")) or -1
    actualSize = getsize(path)
    if actualHash != expectedHash:
        print(f"Hash mismatch! Expected: {expectedHash}, Got: {actualHash}")
    if actualSize != expectedSize:
        print(f"Size mismatch! Expected: {expectedSize}, Got: {actualSize}")
    if actualHash == expectedHash and actualSize == expectedSize:
        return actualHash, actualSize
    return None, None


def getVersion():
    """Determines the version of the program."""
    fileName = args.url.split("/")[-1]
    output = check_output(
        f"7z l -ba -slt -i\!*/WeixinUpdate.exe ./downloads/{fileName}", shell=True
    )
    m = search(r"Path = (\d+\.\d+\.\d+\.\d+)/WeixinUpdate\.exe", output.decode("utf-8"))
    if m:
        return m.group(1)
    return "<unknown>"


def updateJson():
    """Updates `versions.json` if update detected, appending the new version information."""
    with open("versions.json", "r") as f:
        data = load(f)
    print(f"Update detected.")
    data.append(newData)
    with open("versions.json", "w") as f:
        dump(data, f, indent=4)


def generateReleaseNotes():
    """Generate release notes based on the changes."""
    with open("release-notes.md", "w") as f:
        f.write("## Version Info\n")
        f.write(f"- Version: `{newData['version']}`\n")
        f.write(f"- Released: {newData['released']}\n")
        f.write("\n")
        f.write("## Installer\n")
        f.write(f"- Size: {naturalsize(newData['size'])}\n")
        f.write(f"- MD5: `{newData['md5']}`\n")
        f.write("\n")


def main():
    newData["version"] = getVersion()
    md5Hash, size = getStat(args.url, args.url.split("/")[-1])
    newData["md5"] = md5Hash
    newData["size"] = size
    updateJson()
    generateReleaseNotes()
    setOutput("version", newData["version"])


if __name__ == "__main__":
    main()
