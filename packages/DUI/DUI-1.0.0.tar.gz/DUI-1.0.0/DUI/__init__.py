# -*- coding:utf-8 -*-
# @Time    : 2020-4-14
# @Author  : Lettle

from DUI.Frames import *
from DUI.Widgets import *
from DUI.bin import *

def showTestWindow():
	f = Frame("w")
	mainWindow = Window("主界面")

	text1 = Text("DUI库的测试窗口", 0)
	text2 = Text("版本:V0.1.0", 1)
	text3 = Text("作者:Lettle", 1)
	text4 = Text("一起学习?加作者QQ:1071445082", 1)
	text5 = Text("---By Lettle", 2)

	mainWindow.addWidget(2, text1)
	mainWindow.addWidget(4, text2)
	mainWindow.addWidget(6, text3)
	mainWindow.addWidget(8, text4)
	mainWindow.addWidget(10,text5)

	f.addWindow(mainWindow, 0)
	f.showWindow(0)