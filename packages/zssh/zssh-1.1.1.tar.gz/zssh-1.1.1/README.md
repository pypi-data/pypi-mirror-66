# ZSSH - ZIP over SSH
#### Simple Python script to exchange files between servers.

[![PyPI version](https://badge.fury.io/py/zssh.svg)](https://pypi.org/project/zssh)

Login to SSH and choose which path you need to serve over HTTP.

> This script is based on Python 3+

#### Intall from PIP
```sh
python3 -m pip install zssh
```

Expose a directory to `ZIP`
```sh
$ python3 -m zssh -as --path /desktop/path_to_expose
```

Extract a `ZIP` from URL
```sh
$ python3 -m zssh -ad --path /desktop/path_to_download --zip http://mydomain.com/temp_file.zip
```

Usage
```bash
usage: zssh [-h] -a A --path PATH [--zip ZIP] [--port PORT]

required arguments:
  -a A         Action [s = serve, d = download]
  --path PATH  File/Folder Path

optional arguments:
  --zip ZIP    ZIP File URL | Name should be *.zip
  --port PORT  Server Port | Default: 9800
```
