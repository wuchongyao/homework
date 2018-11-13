#!/usr/bin/env python 
# -*- coding:utf-8 -*-


import os 
import openpyxl
import logging
from PIL import Image


material_dir = "D:\\python\\homework3\\material"
picture_style = ['.png', '.jpg', '.jpeg', '.bmp']
box_size = [0, 0, 128, 128]
os.chdir(material_dir)
# print(os.getcwd())


class ImageDeal():
    def __init__(self, table_name):
        self.table_name = table_name


    def select_picture(self):
        "选出目录下的相应类型文件，并返回一个列表，列表的每一项为文件的完整路径"
        file_paths = []
        for paths, dirnames, filenames in os.walk(material_dir):          
            for filename in filenames:
                if os.path.splitext(filename)[1] in picture_style:
                    file_paths.append(filename)
        return file_paths


    def get_picture_info(self):
        "获取相应后缀名的文件名字，后缀名，大小并返回一个字典"
        file_info = {}
        file_paths = self.select_picture()
        for filename in file_paths:
            file_path = material_dir + '\\' + filename
            # print(file_path)
            file_info[os.path.splitext(filename)] = os.path.getsize(file_path)
            # .append(os.path.getsize(filename_dir))
        return file_info


    def stor_info(self):
        "将获取到的信息存到excel表格中，第一列名称、第二列后缀名、第三列大小"
		logger = self.de8ug_log()
        wb = openpyxl.Workbook()
        sh1 = wb.active
        sh1.title = "图片信息"
        files_info = self.get_picture_info()
        name_value = list(files_info.keys())
        size_value = list(files_info.values())
        sh1['A1'] = "名称"
        sh1['B1'] = "后缀名"
        sh1['C1'] = "大小"
        for i in range(len(name_value)):
            sh1[f'A{i+2}'] = name_value[i][0]
            sh1[f'B{i+2}'] = name_value[i][1]
            sh1[f'C{i+2}'] = size_value[i]
        try:
            wb.save(self.table_name)
			logger.info("save successfully")
        except PermissionError as f:
            logger.error(f)


    def image_rotate(self, image_path, degree_value):
        "图片旋转"
        im = Image.open(image_path)
        im.rotate(degree_value).show()
        im.close()


    def image_tailor(self, image_path, box_size):
        "图片裁剪"
        im = Image.open(image_path)
        # print(im.size)
        im.crop(box_size).show()
        im.close()


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
        

def main():
    pic = ImageDeal("picture.xlsx")
    # pic.select_picture()
    # pic.get_picture_info()
    # pic.stor_info()
    # pic.image_rotate(material_dir + "\\" + "picture07.jpg", 540)
    pic.image_tailor(material_dir + "\\" + "picture07.jpg", box_size)


if __name__ == '__main__':
    main()