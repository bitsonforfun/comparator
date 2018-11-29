#!/usr/bin/python
# -*- coding: UTF-8 -*-


from tkinter import *  # 导入 Tkinter 库
import tkinter.filedialog

root = Tk()  # 创建窗口对象的背景色

# def xz():
#     filename = tkinter.filedialog.askopenfilename()
#     if filename != '':
#         lb.config(text="您选择的文件是：" + filename)
#     else:
#         lb.config(text="您没有选择任何文件")
#
#
# lb = Label(root, text='')
# lb.pack()
# btn = Button(root, text="弹出选择文件对话框", command=xz)
# btn.pack()

from tkinter import *
from tkinter.filedialog import askdirectory


def selectPath():
    path_ = askdirectory()
    path.set(path_)


root = Tk()
path = StringVar()

Label(root, text="目标路径:").grid(row=0, column=0)
entry = Entry(root, textvariable=path).grid(row=0, column=1)
Button(root, text="路径选择", command=selectPath).grid(row=0, column=2)

root.mainloop()  # 进入消息循环