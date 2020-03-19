#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Lianghd
import datetime

import matplotlib.pyplot as plt

from CurrencyFund import getWorth
from match import getAllData

# 修改字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# 获取债券型基金数据
def getAllCurrency():
    AllData = getAllData()
    CurrencyCode = []
    CurrencyName = []
    for data in AllData:
        if data[3] == "货币型":
            CurrencyCode.append(data[0])
            CurrencyName.append(data[2])
    return CurrencyCode, CurrencyName


def saveAllCurrency():
    CurrencyCode, CurrencyName = getAllCurrency()

    # 数据导出
    millionCopiesFile = open('货币型基金数据/每万份收益.csv', 'w')
    sevenDaysYearFile = open('货币型基金数据/7日年化收益率.csv', 'w')

    for i in range(len(CurrencyCode)):
        try:
            millionCopies, sevenDaysYear = getWorth(CurrencyCode[i])
        except:
            continue
        if len(millionCopies) <= 0 or len(sevenDaysYear) < 0:
            print(CurrencyCode[i] + "'s' data is empty.")
            continue
        millionCopiesFile.write("\'" + CurrencyName[i] + "\',")
        millionCopiesFile.write("," + CurrencyCode[i] + "\',")
        millionCopiesFile.write(",".join(list(map(str, millionCopies))))
        millionCopiesFile.write("\n")

        sevenDaysYearFile.write("\'" + CurrencyName[i] + "\',")
        sevenDaysYearFile.write("," + CurrencyCode[i] + "\',")
        sevenDaysYearFile.write(",".join(list(map(str, sevenDaysYear))))
        sevenDaysYearFile.write("\n")
        print("write " + CurrencyCode[i] + "'s data success.")

        # 图像导出(新生代基金不足90天)
        if len(millionCopies) > 90:
            totalDays = 90
        else:
            totalDays = len(millionCopies)

        t = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(totalDays)]
        plt.gcf().autofmt_xdate()
        plt.plot(t, millionCopies[:totalDays][::-1])
        plt.title(u"每万元收益")
        if "/" in CurrencyName[i]:
            plt.savefig("货币型基金数据/每万元收益/" + CurrencyCode[i] + ".png")
        else:
            plt.savefig("货币型基金数据/每万元收益/" + CurrencyName[i] + CurrencyCode[i] + ".png")
        plt.clf()

        plt.plot(t, sevenDaysYear[:totalDays][::-1])
        plt.title(u"7日年化收益率")
        if "/" in CurrencyName[i]:
            plt.savefig("货币型基金数据/7日年化收益率/" + CurrencyCode[i] + ".png")
        else:
            plt.savefig("货币型基金数据/7日年化收益率/" + CurrencyName[i] + CurrencyCode[i] + ".png")
        plt.clf()

    millionCopiesFile.close()
    sevenDaysYearFile.close()

    print("Finish")


if __name__ == '__main__':
    saveAllCurrency()
