# -*- coding:utf-8 -*-
import ctypes
import os
from comtypes.client import CreateObject
from win32com.client import Dispatch
from PyGameAuto.Dm import RegDm


class DmHelper:

    def __init__(self, reg_code="", ver_info=""):
        # 方法1
        # dm = RegDm.reg()
        # print('本机系统中已经安装大漠插件，版本为:', dm.ver())
        # 方法2
        try:
            self.dm = Dispatch('dm.dmsoft')
            dm_version = self.dm.ver()
            print('本机系统中已经安装大漠插件，版本为:', dm_version)
            self.dm.reg("jv965720b239b8396b1b7df8b768c919e86e10f", "jvpwigc9jrxz700")
        except:
            print('本机并未安装大漠，正在免注册调用，cmd=' + os.getcwd())
            dms = ctypes.windll.LoadLibrary('DmReg.dll')
            location_dmreg = os.getcwd() + '\dm.dll'
            dms.SetDllPathW(location_dmreg, 0)
            self.dm = CreateObject('dm.dmsoft')
            print('免注册调用成功 版本号为:', self.dm.Ver())
            dm_version = self.dm.ver()
            print(dm_version)  # 输出版本号
        if (reg_code != ""):
            dmRegSult = self.dm.Reg(reg_code, ver_info)
            if dmRegSult == -2:
                print("大漠注册码使用失败,只能是使用免费功能。返回状态码为：", dmRegSult, ",进程没有以管理员方式运行")
            elif dmRegSult == 1:
                print("大漠注册码使用成功")
            elif dmRegSult == 4:
                print("大漠注册码使用失败,只能是使用免费功能。返回状态码为：", dmRegSult, ",注册码错误")
            elif dmRegSult != 1:
                print("大漠注册码使用失败,只能是使用免费功能。返回状态码为：", dmRegSult)

    def getDm(self):
        pass

    def getDm2(self):
        # if not hasattr(self,'dm'):
        # # if(self.dm is None):
        #     print("not have self.dm")
        pass


if __name__ == "__main__":
    dm = Dispatch('dm.dmsoft')
    dm_version = dm.ver()
    print('本机系统中已经安装大漠插件，版本为:', dm_version)
    dm_vip = dm.Reg("jv965720b239b8396b1b7df8b768c919e86e10f", "jvpwigc9jrxz700")

    if dm_vip != 1:
        print(f'收费注册失败！返回值是{dm_vip}。')
    else:
        print(f'收费注册成功！返回值是{dm_vip}。')

    hwnd = dm.EnumWindow(0, "TheRender", "RenderWindow", 1 + 2)
    hwnd = int(hwnd)
    hwnd = hwnd
    print(hwnd,"hwnd")
    str = dm.BindWindowEx(hwnd, "dx.graphic.opengl", "windows", "windows", "", 0)
    print(str,"hwnd1")
    dm.SetPath(path)
    print(hwnd,"hwnd2")
    dm.SetAero(0)
    print(hwnd,"hwnd3")
    dm.Capture(535, 923, 617, 969, "inplay.bmp")
    print(hwnd,"hwnd4")
