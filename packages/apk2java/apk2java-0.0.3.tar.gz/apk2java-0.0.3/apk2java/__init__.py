
from subprocess import call, TimeoutExpired, Popen
import urllib.request
import os
import glob
import shutil
import argparse

def install(path, url):
    package_path = os.path.dirname(os.path.realpath(__file__))
    full_path = package_path + "/" + path
    if os.path.exists(full_path):
        return
    os.mkdir(full_path)
    try:
        name, hdrs = urllib.request.urlretrieve(url)
    except IOError as e:
        print("Can't retrieve %s: %s" % (url, e))
        return
    call(["unzip", name, "-d", full_path])

def install_jd_cli():
    install("tools/jd-cli",
            "https://github.com/kwart/jd-cmd/releases/download/jd-cmd-1.0.1.Final/jd-cli-1.0.1.Final-dist.zip")

def install_dex_tools():
    install("tools/dex-tools",
            "https://github.com/pxb1988/dex2jar/files/1867564/dex-tools-2.1-SNAPSHOT.zip")

def setup():
    package_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(package_path + "/tools"):
        os.mkdir(package_path + "/tools")
    install_dex_tools()
    install_jd_cli()

def decompile(apk, dir):
    package_path = os.path.dirname(os.path.realpath(__file__))
    if not os.path.exists(dir):
        os.mkdir(dir)
    basename = os.path.basename(apk)
    call(["apktool", "-f", "d", apk, "-o", "%s/%s" % (dir, basename)])
    call(["unzip", apk, "-d", "%s/%s/zip" % (dir, basename)])
    call([glob.glob(package_path + "/tools/dex-tools/*/d2j-dex2jar.sh")[0],
        "%s/%s/zip/classes.dex"\
        % (dir, basename), "-o", "%s/%s/zip/apk.jar" % (dir, basename)])
    try:
        p = Popen(["java", "-jar", package_path + "/tools/jd-cli/jd-cli.jar", "-od", "%s/%s/src/" % (dir, basename) ,"-sr",
        "%s/%s/zip/apk.jar" % (dir, basename)], shell=False) 
        p.communicate(timeout=30)
    except TimeoutExpired:
        p.kill()
        p.communicate()
        p.wait()
        print("Maybe the decompilation is imcomplete")
        return p.pid
    return 0

def main():
    parser = argparse.ArgumentParser(description='apk2java convert apk to java')
    parser.add_argument('apk', type=str, help='path to apk')
    parser.add_argument('dir', type=str, help='path to decompile')

    args = parser.parse_args()

    return decompile(args.apk, args.dir)

