#!/usr/bin/env python3

import os
import sys
import argparse
import glob
import shutil
import http.server
import socketserver
import requests
import urllib.request
from zipfile import ZipFile
from urllib.parse import urlparse
import hashlib
import time

handler = http.server.SimpleHTTPRequestHandler


def server(args):

    temp_dir = '/tmp/tserver'
    port = int(args.port)
    path = args.path
    hash_name = hashlib.md5(str(time.time()).encode()).hexdigest().upper()

    print("")
    print("Ziping files...")

    if os.path.exists(path):
        os.chdir(path)

        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        os.mkdir(temp_dir)

        with ZipFile(temp_dir + '/' + hash_name + '.zip', 'w') as mzip:
            for folderName, subfolders, filenames in os.walk('.'):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    mzip.write(filePath)

    os.chdir(temp_dir)

    print("Fetching IP address...")

    ip = "127.0.0.1"
    try:
        req = requests.get('https://postman-echo.com/ip', timeout=10)
        ip = req.json()['ip']
    except:
        print("Fetching IP address failed.")

    f = open(temp_dir + '/index.html', "w")
    f.write("<i>Exposed.</i>")
    f.close()

    with socketserver.TCPServer(("0.0.0.0", port), handler) as httpd:

        download_url = "http://" + ip + ":" + str(port) + "/" + hash_name + ".zip"

        print("\n$ python3 -m zssh -ad --zip " + download_url + " --path [PATH]\n")

        try:
            httpd.serve_forever()
        except:
            print("Closing the server.")
            httpd.shutdown()
            httpd.server_close()
            raise

    print("")


def client(args):

    print("")
    zip_url = args.zip
    path = args.path
    file = "/tmp/" + zip_url.split('/')[-1]

    if "[" in path:
        print("Please choose valid path.\n")
        return

    if ".zip" not in file:
        print("Please enter valid zip file URL.\n")
        return

    print("Donwloading file...")

    try:
        urllib.request.urlretrieve(zip_url, file)
        print("Extracting zip file...")
        with ZipFile(file, 'r') as mzip:
            mzip.extractall(path)
        os.unlink(file)
        print("\nSuccesfully extracted " + zip_url + " --> " + path)
    except:
        print("The URL is no longer accessibles.")
    print("")


def main():

    try:
        parser = argparse.ArgumentParser()
        parser._action_groups.pop()

        required = parser.add_argument_group('required arguments')
        optional = parser.add_argument_group('optional arguments')

        required.add_argument("-a", required=True, help="Action [s = serve, d = download]")
        required.add_argument("--path", help="File/Folder Path", required=True)

        optional.add_argument("--zip", help="ZIP File URL | Name should be *.zip")
        optional.add_argument("--port", help="Server Port | Default: 9800", default="9800", type=int)

        args = parser.parse_args()

        if args.a == "s":
            server(args)

        if args.a == "d":
            client(args)

    except KeyboardInterrupt:
        print("System exited.")


if __name__ == "__main__":
    main()
