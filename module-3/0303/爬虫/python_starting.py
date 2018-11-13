#!/usr/bin/env python
# -*- coding:utf-8 -*-
# author:wuchongyao
# date:2018-09-17
# 开始学习爬虫

import logging
import os
import requests
import csv
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import jieba
import jieba.analyse
import re


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILENAME = BASE_DIR + '\\' + 'test.csv'
STOP_WORD_FILE = BASE_DIR + '\\' + 'stop_words.txt'
LOG_FILE = BASE_DIR + '\\' + 'wcy.log'
TEST_URL = r"http://detail.zol.com.cn/1208/1207038/review.shtml"


class BadCommentAnalyse:
    def __init__(self):
        self.num_retries = 3

    def download(self, url, is_json=False):
        '''下载页面'''
        print('下载页面:', url)
        # self.throttle.wait(url)
        try:
            # response = requests.get(url, headers=self.headers, proxies=self.proxies, timeout=self.timeout)
            response = requests.get(url)
            print(response.status_code)
            if response.status_code == 200:
                temp_code = response.encoding
                if is_json:
                    return response.json()
                else:
                    return response.content.decode(temp_code)
            return None
        except RequestException as e:
            print('error:', e.response)
            html = ''
            if hasattr(e.response, 'status_code'):
                code = e.response.status_code
                print('error code:', code)
                if self.num_retries > 0 and 500 <= code < 600:
                    # 遇到5XX 的错误就重试
                    html = self.download(url)
                    self.num_retries -= 1
            else:
                code = None
        return html

    def featch_data(self):
        '''抓取评价信息'''
        logger = self.de8ug_log()
        data = []
        # information = {}
        html = self.download(TEST_URL)
        soup_all = BeautifulSoup(html, 'lxml')
        len_valuer_list = len(soup_all.find_all('div', attrs={'class': 'comments-item'}))
        for i in range(len_valuer_list):
            # print(i)
            soup_user = soup_all.find_all('div', attrs={'class': 'comments-item'})[i].find('div', attrs={'class': 'comments-user'})
            name = soup_user.find('a', attrs={'class': 'name'}).string
            print(name)
            key = soup_user.find('p').string
            value = soup_user.find_all('p')[1].string + '\n' + soup_user.find_all('p')[2].string + '\n' + soup_user.find_all('p')[3].string
            # information[key] = value
            soup_content_list = soup_all.find_all('div', attrs={'class': 'comments-item'})[i].find('div', attrs={'class': 'comment-list-content'})
            try:
                if soup_content_list.find_all('div', attrs={'class': 'words'})[0].find('strong').string == '优点：':
                    good_feedback = soup_content_list.find_all('div', attrs={'class': 'words'})[0].find('p').string
                    try:
                        if soup_content_list.find_all('div', attrs={'class': 'words'})[1].find('strong').string == '缺点：':
                            bad_feedback = soup_content_list.find_all('div', attrs={'class': 'words'})[1].find('p').string
                    except Exception as identifier:
                        logger.error("no bad feedback")
                        bad_feedback = "no feedback"
            except Exception as identifier:
                logger.error("no good feedback")
                good_feedback = "no feedback"
                try:
                    if soup_content_list.find_all('div', attrs={'class': 'words'})[0].find('strong').string == '缺点：':
                        bad_feedback = soup_content_list.find_all('div', attrs={'class': 'words'})[1].find('p').string
                except Exception as identifier:
                    logger.error("no bad feedback")
                    bad_feedback = "no feedback"
            user_data = [name, key+':'+value, good_feedback, bad_feedback]
            data.append(user_data)
        logger.info("featch data successfully")
        return data

    def save_csv_file(self, filename, all_list):
        '''保存数据'''
        with open(filename, 'w', newline='') as f:
            writer = csv.writer(f)
            fields = ('id', 'information', '好评', '差评')
            writer.writerow(fields)
            for row in all_list:
                writer.writerow(row)

    def get_all_text(self, filename):
        """取出所有评价的句子
        """
        comment_list = []
        with open(filename) as f:
            rows = csv.reader(f)
            for row in rows:
                # print(row)
                one_comment = row[-1]
                # print(one_comment)
                comment_list.append(one_comment)

        return ''.join(comment_list[1:]) 

    def cut_text(self, all_text):
        """找到评价中重要关键词
        """
        # https://github.com/fxsjy/jieba
        jieba.analyse.set_stop_words(STOP_WORD_FILE)
        text_tags = jieba.analyse.extract_tags(all_text, topK=30)
        return text_tags

    def get_bad_words(self, text_tags, all_text):
        """根据关键词找到对应的句子
        """
        words = {}
        for tag in text_tags:
            tag_re = re.compile(f'(\w*{tag}\w*)')
            # print(tag_re.findall(all_text))
            words[tag] = tag_re.findall(all_text)
        return words

    @staticmethod
    def de8ug_log(logger_name='WCY-LOG', log_file=LOG_FILE, level=logging.DEBUG):
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


def main():
    bad1 = BadCommentAnalyse()
    # html = bad1.download(TEST_URL)
    data = bad1.featch_data()
    bad1.save_csv_file(FILENAME, data)
    all_text = bad1.get_all_text(FILENAME)
    # print(all_text)
    text_tags = bad1.cut_text(all_text)
    # print(text_tags)
    words = bad1.get_bad_words(text_tags, all_text)
    print(words)
    # print(html)
    # print(data)


if __name__ == "__main__":
    main()
