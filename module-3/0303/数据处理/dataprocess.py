#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# func:数据采集、保存；office文件处理；图片操作
# wuchongyao in shenzhen 2018-09-19


from PIL import Image
import logging
import docx
import pickle
import os
import requests
from bs4 import BeautifulSoup
import json


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
print(BASE_DIR)
USERS_CONFIG_DIR = BASE_DIR + r'\user_config'
print(USERS_CONFIG_DIR)
USERS_LOG_DIR = BASE_DIR + r'\log'
print(USERS_LOG_DIR)
USERS_DATA_DIR = BASE_DIR + r'\data'
print(USERS_DATA_DIR)

if not os.path.exists(USERS_CONFIG_DIR):
    os.mkdir(USERS_CONFIG_DIR)
USERS_CONFIG_FILE = USERS_CONFIG_DIR + '\\' + 'user_config.pkl'

if not os.path.exists(USERS_LOG_DIR):
    os.mkdir(USERS_LOG_DIR)

if not os.path.exists(USERS_DATA_DIR):
    os.mkdir(USERS_DATA_DIR)

TEST_IMAGE = BASE_DIR + "\\" + "test.jpg"

if not os.path.exists(USERS_CONFIG_FILE):
    with open(USERS_CONFIG_FILE, 'w') as f:
        f.write('username password')


def auth_user(func):
    def iden_user(self):
        "用户认证，第一个用户默认注册为ADMIN role"
        logger = self.log_wcy()
        with open(USERS_CONFIG_FILE, 'rb') as f:
            try:
                user_info = pickle.load(f)
                for temp in user_info:
                    user_name = temp.strip().split()[0]
                    user_password = temp.strip().split()[1]
                    user_role = temp.strip().split()[2]
                    if user_name == self.name:
                        if user_password == self.password:
                            logger.info("login successfully")
                            return user_role
                        else:
                            logger.error("please check your password")
                            exit(2)

                logger.error(f"no user {self.name} exist")
                user_awk = input('would you like to register(y/n):')
                if user_awk == 'y':
                    register_user(self.name, self.password, "USER")
                    logger.info(f"{self.name} register as USER successfully, auto exit")
                    exit(0)
                else:
                    exit(1)
            except Exception as e:
                register_user(self.name, self.password, "ADMIN")
                logger.info(f"{self.name} register as ADMIN successfully, auto exit")
                exit(3)
    return iden_user


def register_user(name, password, role):
    if role == "USER":
        users_info = f_read(USERS_CONFIG_FILE)

    else:
        users_info = []
    user_info = name + ' ' + password + ' ' + role
    users_info.append(user_info)
    datafile = USERS_DATA_DIR + '\\' + name + '.json'
    init_data = {"user": {"name": name, "password": password, "role": role}}
    with open(USERS_CONFIG_FILE, 'wb') as f1:
        pickle.dump(users_info, f1)
    with open(datafile, 'w') as f2:
        json.dump(init_data, f2)


def f_read(file_name):
    '''从文件读取memo'''
    data = ''
    f3 = open(file_name, 'rb')
    try:
        data = pickle.load(f3)
    except EOFError:
        print("ran out of input")
    except (TypeError, pickle.UnpicklingError):
        return data
    return data


def f_write(comment, file_name):
    '''写入文件'''
    with open(file_name, 'wb') as f5:
        pickle.dump(comment, f5)


class DataClass():
    def __init__(self, name, password):
        self.name = name
        self.password = password

    @auth_user
    def test_auth_user(self):
        print("test decorator !")

    @staticmethod
    def del_user(username):
        with open(USERS_CONFIG_FILE, 'rb') as f:
            try:
                user_info = pickle.load(f)
                # print(user_info)
                for temp in user_info:
                    user_name = temp.strip().split()[0]
                    user_password = temp.strip().split()[1]
                    user_role = temp.strip().split()[2]
                    if user_name == username:
                        # print(user_info)
                        # print(temp)
                        user_info.remove(temp)
                        # print(new_user_info)
                        f_write(user_info, USERS_CONFIG_FILE)
                        datafile = USERS_DATA_DIR + '\\' + username + '.json'
                        logfile = USERS_LOG_DIR + '\\' + username + '.' + 'log'
                        if os.path.exists(datafile):
                            os.remove(datafile)
                            os.remove(logfile)
                        else:
                            print(f"{datafile} not exist")
                        print(f"del user {username} successfully")
                        exit(0)
            except Exception as e:
                print(f"no {username} exist!")

    def log_wcy(self):
        logger = logging.getLogger(USERS_LOG_DIR + '\\' + self.name + '.' + 'log')
        logger.setLevel(logging.DEBUG)

        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)

        # 创建文件 handler
        fh = logging.FileHandler(filename=USERS_LOG_DIR + '\\' + self.name + '.' + 'log', encoding='utf-8')
        # fh.setLevel(logging.)

        # 创建 formatter
        formatter = logging.Formatter('%(asctime)s %(filename)s [line:%(lineno)d] %(name)s %(levelname)s %(message)s')

        # 添加 formatter
        ch.setFormatter(formatter)
        fh.setFormatter(formatter)

        # 把 ch， fh 添加到 logger
        logger.addHandler(ch)
        logger.addHandler(fh)

        return logger

    @staticmethod
    def get_data(url):
        src_dict = {}
        session = requests.session()
        html = session.get(url).content
        soup = BeautifulSoup(html, 'lxml')
        for tag in soup.find_all('img'):
            try:
                src_dict[tag['alt']] = tag['src'] + "\n"
            except Exception as e:
                continue
        return src_dict

    def save_data(self, src_dict):
        print("________________________________________________")
        user_data_file = USERS_DATA_DIR + '\\' + self.name + '.json'
        with open(user_data_file, 'r') as f:
            user_data = json.load(f)
            try:
                user_data['operation']['crawler'] = str(user_data['operation']['crawler']) + str(src_dict)
            except Exception as e:
                print(e)
                user_data['operation'] = {}
                user_data['operation']['crawler'] = src_dict
        with open(USERS_DATA_DIR + '\\' + self.name + '.json', 'w') as f1:
            json.dump(user_data, f1)


class PictureClass():
    def __init__(self, name, password):
        self.name = name
        self.password = password

    def picture_size(self, ratio, path, name):
        # print(path)
        ratio = float(ratio)
        im = Image.open(path)
        width, height = im.size
        im.thumbnail((width*ratio, height*ratio))
        new_name = USERS_DATA_DIR + "\\" + name
        im.save(new_name)

    def picture_rotate(self, angle, path, name):
        new_name = USERS_DATA_DIR + "\\" + name
        im = Image.open(path)
        im.rotate(int(angle)).save(new_name)


def main():
    name = input("please input memo name:")
    passwd = input("please input password:")
    crawler = DataClass(name, passwd)
    # "http://mobile.zol.com.cn/")
    picture = PictureClass(name, passwd)
    user_role = crawler.test_auth_user()
    while True:
        if user_role == "ADMIN":
            beha = input("1: crawler, 2: picture, 3:del user, q:退出\n")
            if beha == '3':
                "删除用户"
                username = input("the user deleted:\n")
                DataClass.del_user(username)
        else:
            beha = input("1: crawler, 2: picture, q:退出\n")
        if beha == 'q':
            break
        else:
            if beha == '1':
                try:
                    method = input("1: getting data, 2: save_data, q:退出\n")
                    url = input("the url of data source\n")
                    if method == '1':
                        crawler.get_data(url)
                    elif method == '2':
                        src_dict = crawler.get_data(url)
                        crawler.save_data(src_dict)
                    else:
                        break
                except Exception as e:
                    continue
            elif beha == '2':
                method = input("1: set size, 2: ratito, q:退出\n")
                if method == '1':
                    ratio = input("the ratio of image\n")
                    name = input("the name to save\n")
                    path = TEST_IMAGE
                    picture.picture_size(ratio, path, name)
                elif method == '2':
                    angle = input("the angle of image\n")
                    name = input("the name to save\n")
                    path = TEST_IMAGE
                    picture.picture_rotate(angle, path, name)
                else:
                    break


if __name__ == '__main__':
    main()
