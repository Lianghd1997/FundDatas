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

    # 每万份收益
    millionCopiesIncome = jsContent.eval('Data_millionCopiesIncome')
    # 七日年化收益率
    sevenDaysYearIncome = jsContent.eval('Data_sevenDaysYearIncome')

    millionCopies = []
    sevenDaysYear = []

    # 提取净值和7日年化收益
    for dayIncome in millionCopiesIncome[::-1]:
        millionCopies.append(dayIncome[1])

    for day7Income in sevenDaysYearIncome[::-1]:
        sevenDaysYear.append(day7Income[1])

    print(name, code)
    return millionCopies, sevenDaysYear


# 债券型基金查询
def getMonetary():
    print("请输入需要查询的货币型基金代码：")
    codeInput = input()
    millionCopies, sevenDaysYear = getWorth(codeInput)
    t = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(90)]
    plt.gcf().autofmt_xdate()
    plt.plot(t, millionCopies[:90][::-1])
    plt.title(u"每万元收益")
    plt.show()

    plt.plot(t, sevenDaysYear[:90][::-1])
    plt.title(u"7日年化收益率")
    plt.show()


if __name__ == '__main__':
    getMonetary()
