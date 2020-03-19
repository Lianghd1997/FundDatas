#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Lianghd

import requests
import execjs
import matplotlib.pyplot as plt
import datetime
from pandas.plotting import register_matplotlib_converters

from match import getUrl

# 更改字体样式
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def getWorth(fscode):
    content = requests.get(getUrl(fscode))

    # 用execjs获取到相应的数据
    jsContent = execjs.compile(content.text)
    name = jsContent.eval('fS_name')
    code = jsContent.eval('fS_code')

    # 单位净值走势
    netWorthTrend = jsContent.eval('Data_netWorthTrend')
    # 累计净值走势
    ACWorthTrend = jsContent.eval('Data_ACWorthTrend')

    netWorth = []
    ACWorth = []

    # 提取单位净值和累计净值
    for dayWorth in netWorthTrend[::-1]:
        netWorth.append(dayWorth['y'])

    for dayACWorth in ACWorthTrend[::-1]:
        ACWorth.append(dayACWorth[1])

    print(name, code)
    return netWorth, ACWorth


# 货币型基金查询
def getBond():
    print("请输入需要查询的债券型基金代码：")
    codeInput = input()
    netWorth, ACWorth = getWorth(codeInput)

    # 单位净值走势和累计净值走势
    t = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(90)]
    plt.gcf().autofmt_xdate()
    y1 = netWorth[:90][::-1]
    plt.plot(t, y1, label='netWorth')
    y2 = ACWorth[:90][::-1]
    plt.plot(t, y2, label='ACWorth')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    getBond()
