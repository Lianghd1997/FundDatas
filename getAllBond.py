#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Lianghd
import datetime
import matplotlib.pyplot as plt

from BondFund import getWorth
from match import getAllData

# 修改字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


# 获取债券型基金数据
def getAllBond():
    AllData = getAllData()
    BondCode = []
    BondName = []
    for data in AllData:
        if data[3] == "债券型":
            BondCode.append(data[0])
            BondName.append(data[2])
    return BondCode, BondName


def saveAllBond():
    BondCode, BondName = getAllBond()

    netWorthFile = open('债券型基金数据/单位净值.csv', 'w')
    ACWorthFile = open('债券型基金数据/累计净值.csv', 'w')

    for i in range(len(BondCode)):
        try:
            netWorth, ACWorth = getWorth(BondCode[i])
        except:
            continue
        if len(netWorth) <= 0 or len(ACWorth) < 0:
            print(BondCode[i] + "'s' data is empty.")
            continue
        netWorthFile.write("\'" + BondName[i] + "\',")
        netWorthFile.write("," + BondCode[i] + "\',")
        netWorthFile.write(",".join(list(map(str, netWorth))))
        netWorthFile.write("\n")

        ACWorthFile.write("\'" + BondName[i] + "\',")
        ACWorthFile.write("," + BondCode[i] + "\',")
        ACWorthFile.write(",".join(list(map(str, ACWorth))))
        ACWorthFile.write("\n")
        print("write " + BondCode[i] + "'s data success.")

        # 图像导出(新生代基金不足90天)
        if len(netWorth) > 90:
            totalDays = 90
        else:
            totalDays = len(netWorth)

        t = [datetime.datetime.now() - datetime.timedelta(days=i) for i in range(totalDays)]
        plt.gcf().autofmt_xdate()

        plt.plot(t, netWorth[:totalDays][::-1])
        plt.title(u"单位净值")
        if "/" in BondName[i]:
            plt.savefig("债券型基金数据/单位净值走势图/" + BondCode[i] + ".png")
        else:
            plt.savefig("债券型基金数据/单位净值走势图/" + BondName[i] + BondCode[i] + ".png")
        plt.clf()

        plt.plot(t, ACWorth[:totalDays][::-1])
        plt.title(u"累计净值")
        if "/" in BondName[i]:
            plt.savefig("债券型基金数据/累计净值走势图/" + BondCode[i] + ".png")
        else:
            plt.savefig("债券型基金数据/累计净值走势图/" + BondName[i] + BondCode[i] + ".png")
        plt.clf()

    netWorthFile.close()
    ACWorthFile.close()

    print("Finish")


if __name__ == '__main__':
    saveAllBond()
