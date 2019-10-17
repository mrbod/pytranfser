#!/usr/bin/env python3
import sys
import os
import io
import pathlib
import argparse
import requests
import subprocess as sp

def send_stream(name, fp):
    '''send file to transfer.sh'''
    r = requests.put(f'https://transfer.sh/{name}', data=fp, timeout=60)
    r.raise_for_status()
    return r

def send_zip(path):
    '''make a zip archive of directory "path" and send_it'''
    zip_prg = 'zip'
    args = [zip_prg, '-r', '-q', '-', '.']
    try:
        proc = sp.Popen(args, stdout=sp.PIPE, stderr=sp.PIPE, cwd=path)
    except Exception as e:
        raise Exception(f'unable to execute command: {" ".join(args)}\n{e}')
    result = send_stream(path.name + '.zip', proc.stdout)
    exit_status = proc.wait()
    if exit_status != 0:
        s = proc.stderr.read()
        raise Exception(f'zip failed({exit_status}):\n{s}')
    return result

def send(filename='foo', **kwargs):
    '''send path to transfer.sh

    * if filename is a file, send it
    * if filename is a directory, zip it up and send it
    * if something is piped on stdin, send it using filename
    '''
    path = pathlib.Path(filename)
    if not sys.stdin.isatty():
        return send_stream(path.name, sys.stdin.buffer)
    if path.is_file():
        return send_stream(path.name, path.open(mode='rb'))
    if path.is_dir():
        return send_zip(path)
    raise Exception(f'invalid filename: {filename}')

def main():
    '''Upload to transfer.sh'''
    p = argparse.ArgumentParser(description=main.__doc__)
    p.add_argument('filename', help='file/dir to upload')
    args = p.parse_args()
    r = send(**vars(args))
    print(r.content.decode('utf-8'))
    #for k, v in r.headers.items():
    #    print(k, v)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f'transfer failed: {e}', file=sys.stderr)
        sys.exit(1)
