#!/usr/bin/env python
# -*- coding:utf-8 -*-
# 51memo_v028.py
# a memo demo 51备忘录，使用类
# author:wcy


import pickle
import os
import logging
import time
import json
import smtplib
import email
from email.mime.text import MIMEText
from email.header import Header
from email.mime.base import MIMEBase
from email import encoders


password = "qiywedvqlbxxijag"
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
print(BASE_DIR)
USERS_CONFIG_DIR = BASE_DIR + '/user_config'

if not os.path.exists(USERS_CONFIG_DIR):
    os.mkdir(USERS_CONFIG_DIR)
USERS_CONFIG_FILE = USERS_CONFIG_DIR + '/user_config.pkl'

if not os.path.exists(USERS_CONFIG_FILE):
    with open(USERS_CONFIG_FILE, 'w') as f:
        f.write('username password')


class Memo(object):
    def __init__(self, name, password,  thing= None, date=None):
        '''初始化'''
        self.__kid = 1
        self.name = name
        self.thing = thing
        self.date = date
        self.password = password
        self.datafile = USERS_CONFIG_DIR + '/' + name + '.pkl'

    @property
    def cal_id(self):
        return self.__kid


class MemoAdmin(Memo):
    def add(self, thing, date):
        '''增加事件'''
        u_key = []
        i = 0
        memolist = list(f_read(self.datafile))
        try:
            for memo_dict in memolist:
                (key, value), = memo_dict.items()
                u_key.append(key)
                i += 1
            memo_dict = {self.cal_id + int(max(u_key)): f'{self.name}\
{thing} {date}'}
        except ValueError:
            print("no memo list in memolist")
            memo_dict = {self.cal_id: f'{self.name}\
{thing} {date}'}
        memolist.append(memo_dict)
        print(memolist)
        f_write(memolist, self.datafile)


    # @staticmethod
    def delete(self, memo_kid):
        '''删除事件'''
        memolist = list(f_read(self.datafile))
        print(f'删除前:\n{memolist}')
        for memo_dict in memolist:
            (key, value), = memo_dict.items()
            if int(memo_kid) == key:
                memolist.pop(memolist.index(memo_dict))
        print(f'删除后:\n{memolist}')
        f_write(memolist, self.datafile)


    # @staticmethod
    def modify(self, memo_kid, thing, date):
        '''修改事件'''
        memolist = f_read(self.datafile)
        print(f'修改前:\n{memolist}')
        for memo_dict in memolist:
            (key, value), = memo_dict.items()
            if int(memo_kid) == key:
                memo_dict[key] = f'{self.name} {thing} {date}'
        print(f'修改后:\n{memolist}')
        f_write(memolist, self.datafile)


    # @staticmethod
    def query(self, memo_kid):
        '''查询事件'''
        memolist = f_read(self.datafile)
        for memo_dict in memolist:
            (key, value), = memo_dict.items()
            if int(memo_kid) == key:
                print(memo_dict)


    def query_by_month(self, month):
        '''查询事件'''
        temp_dict = {}
        memolist = f_read(self.datafile)
        for memo_dict in memolist:
            (key, value), = memo_dict.items()
            a = value.split(' ')[1].split('-')[1]
            if int(a) == int(month):
                temp_dict[key] = value
        return ConfigAdmin.send_mail(month, json.dumps(temp_dict))


class ConfigAdmin(MemoAdmin):
    def auth_user(self):
        '''认证并注册'''
        logger = self.de8ug_log()
        with open(USERS_CONFIG_FILE, 'rb') as f:
            try:
                user_info = pickle.load(f)
                print(user_info)
                user_name = user_info.strip().split()[0]
                user_password = user_info.strip().split()[1]
                if user_name == self.name:
                    if user_password == self.password:
                        logger.info("login successfully")
                    else:
                        logger.error("please check your password")
                        exit(1)
                else:
                    logger.error(f"no user {self.name} exist")
                    user_awk = input('would you like to register(y/n):')
                    if user_awk == 'y':
                        user_info = list(f_read(USERS_CONFIG_FILE))
                        new_userinfo = self.name + ' ' + self.password
                        user_info.append(new_userinfo)
                        with open(USERS_CONFIG_FILE, 'wb') as f3:
                            pickle.dump(user_info, f3)
                        with open(self.datafile, 'wb') as f1:
                            pass
                    else:
                        exit(2)
            except (TypeError, pickle.UnpicklingError):
                user_awk = input('would you like to register(y/n):')
                if user_awk == 'y':
                    new_userinfo = self.name + ' ' + self.password
                    with open(USERS_CONFIG_FILE, 'wb') as f4:
                        pickle.dump(new_userinfo, f4)
                    with open(self.datafile, 'wb') as f1:
                        pass
                    # pickle.dump(f'This is data file of {self.name}', f1)
                else:
                    exit(3)


    @staticmethod
    def de8ug_log(logger_name='WCY-LOG', log_file='wcy.log', level=logging.DEBUG):
        # 创建 logger对象
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)  # 添加等级

        # 创建控制台 console handler
        ch = logging.StreamHandler()
        ch.setLevel(level)

        # 创建文件 handler
        fh = logging.FileHandler(filename=log_file, encoding='utf-8')

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
    def send_mail(month, comment):
        smtp = smtplib.SMTP_SSL("smtp.qq.com")
        smtp.ehlo("smtp.qq.com")

        print(comment)
        smtp.login("1264718520@qq.com", password)
        msg = MIMEText(comment, 'plain', 'utf-8')
        msg["Subject"] = Header(f'查询结果-{month}月', 'utf-8')
        msg["from"] = "1264718520@qq.com"
        msg["to"] = "15850687669@163.com"
        smtp.sendmail("1264718520@qq.com", "15850687669@163.com", msg.as_string())
        
        smtp.quit()

def f_write(comment, file_name):
    '''写入文件'''
    with open(file_name, 'wb') as f2:
        pickle.dump(comment, f2)
    # fw.close()


def f_read(file_name):
    '''从文件读取memo'''
    # if os.path.exists(db.pkl)
    # with open('db.pkl', 'rb') as f3:
    data = ''
    f3 = open(file_name, 'rb')
    try:
        data = pickle.load(f3)
    except EOFError:
        print("ran out of input")
    return data


def main():
    name = input("please input memo name:")
    passwd = input("please input password:")
    Config = ConfigAdmin(name, passwd)
    Config.auth_user()
    while True:
        date = time.strftime("%Y-%m-%d %X", time.localtime())
        beha = input("1: add, 2: delete, 3: modify, 4: query, q:退出\n")
        if beha == 'q':
            break
        else:
            if beha == '1':
                thing = input("please input memo in thing format:")
                Config.add(thing, date)

            elif beha == '2':
                memo_kid = input("please input the memo kid:")
                Config.delete(memo_kid)

            elif beha == '3':
                thing = input("please input memo in thing format:")
                memo_kid = input("please input the memo kid:")
                Config.modify(memo_kid, thing, date)

            elif beha == '4':
                # memo_kid = input("please input the memo kid:")
                # Config.query(memo_kid)
                test_month = input("please input the month:")
                Config.query_by_month(test_month)


if __name__ == '__main__':
    main()
