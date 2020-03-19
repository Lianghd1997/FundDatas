#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Lianghd

import time

import execjs
import requests


# execjs由python2编写，存在编码问题
# subprocess.py中Popen类的__init__，设置encoding='utf-8'

# 获取实时的基金js文件
def getUrl(fscode):
    head = 'http://fund.eastmoney.com/pingzhongdata/'
    tail = '.js?v=' + time.strftime("%Y%m%d%H%M%S", time.localtime())
    fsUrl = head + fscode + tail
    # print(fsUrl)
    return fsUrl


# 获取全部基金数据
def getAllData():
    url = 'http://fund.eastmoney.com/js/fundcode_search.js'
    response = requests.get(url)

    jsContent = execjs.compile(response.text)
    try:
        allData = jsContent.eval('r')
        print(allData)
    except IndexError:
        pass
    return allData


def match():
    allData = getAllData()
    allCode = []
    allName = []
    allType = []
    for data in allData:
        allCode.append(data[0])
        allName.append(data[2])
        allType.append(data[3])
    print(allCode)
    print(allName)
    print("请输入需要查询的基金代码：")
    codeInput = input()
    if codeInput == "exit":
        print("退出")
    else:
        for i in range(len(allCode)):
            if codeInput == allCode[i]:
                print("对应基金名称为'%s'，类型为'%s'" % (allName[i], allType[i]))
                match()


if __name__ == '__main__':
    match()
