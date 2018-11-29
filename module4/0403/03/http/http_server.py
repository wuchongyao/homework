#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: wuchongyao
# email: wuchongyao@outlook.com
# Date: 2018-11-1
# http_server.py

import os
import socket
import struct


BASE_DIR, FILENAME = os.path.split(os.path.abspath(__file__))
#print(f"base dir: {BASE_DIR}")

HOST = ''
PORT = 8888
ADDR = (HOST, PORT)
BUFSIZE = 1024

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

sock.bind(ADDR)
sock.listen(1)

def deal_response(path):
    if path == "/":
        response = "succsessfully".encode()
    elif path == "/json":
        response = '''{"name": "volume",
        "uuid": "56539f2d-fa3b-3486-8b38-e03bba3bbef8",
        "type": None}'''.encode()
    elif "/pic/" in path:
        pic = BASE_DIR + path
        #fileinfo_size = struct.calcsize('128sl')
        #response = struct.pack('128sl',os.path.basename(pic).encode(), os.stat(pic).st_size)
        response = open(pic, "rb").read()
        #response = f"""HTTP/1.1 200 OK
        #
        #    <h1>hello {path}</h1>
        #    <img src={BASE_DIR}{path}>"""
    else:
        response = "addr is invaild".encode()
    # import pdb;pdb.set_trace()
    return response

def start_server():
    while True:
        print ('waitting for connect......')
        conn, addr = sock.accept()
        print ('successfully connection......')
        data = conn.recv(BUFSIZE)
        if data:
            req_path = data.decode('utf-8').splitlines()[0]
            print ('receive data: ', req_path)
            method, path , http = req_path.split()
            # print(path)
            # response = '''successfully'''.encode()
            conn.sendall(deal_response(path))
        conn.close()

def main():
    #sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #sock.bind(ADDR)
    #sock.listen(3)
    start_server()
    sock.close()

if __name__ == '__main__':
    main()
