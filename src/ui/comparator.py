#!/usr/bin/python
# -*- coding: UTF-8 -*-

import threading
import tkinter as tk

from tkinter import *
from tkinter.filedialog import askdirectory

from src.common import util
from src.compare.comparator import JsonComparator


class Comparator(tk.Frame):
    result_path = ''
    total_counter = 0
    invalid_counter = 0

    t1 = None

    debug = True
    platform = 'mac'

    def __init__(self):
        super().__init__()
        self.pack()

        self.path0 = StringVar()
        self.path1 = StringVar()
        self.path2 = StringVar()
        self.path3 = StringVar()
        self.alert_text = StringVar()

        if self.debug:
            if self.platform == 'mac':
                self.path0.set("/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果1")
                self.path1.set("/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果2")
                self.path2.set("/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/图片")
                self.path3.set("/Users/bitsonli/Desktop/projects/data/脱发分类试标结果")
            elif self.platform == 'win':
                self.path0.set("E:\data\同一组图片两份标注结果\脱发分类试标结果\结果1")
                self.path1.set("E:\data\同一组图片两份标注结果\脱发分类试标结果\结果2")
                self.path2.set("E:\data\同一组图片两份标注结果\脱发分类试标结果\图片")
                self.path3.set("E:\data\同一组图片两份标注结果\脱发分类试标结果")

        # 两个按钮
        self.rowframe0 = tk.Frame(self)
        self.rowframe0.pack(fill='x')
        self.btn0 = tk.Button(self.rowframe0, text='选择结果1的目录', width=12, command=self.btn0_click)
        self.btn0.pack(side=tk.LEFT)
        self.entry0 = tk.Entry(self.rowframe0, width=40, textvariable=self.path0)
        self.entry0.pack(side=LEFT)

        self.rowframe1 = tk.Frame(self)
        self.rowframe1.pack(fill='x')
        self.btn1 = tk.Button(self.rowframe1, text='选择结果2的目录', width=12, command=self.btn1_click)
        self.btn1.pack(side=tk.LEFT)
        self.entry1 = tk.Entry(self.rowframe1, width=40, textvariable=self.path1)
        self.entry1.pack(side=LEFT)

        self.rowframe2 = tk.Frame(self)
        self.rowframe2.pack(fill='x')
        self.btn2 = tk.Button(self.rowframe2, text='选择图片目录', width=12, command=self.btn2_click)
        self.btn2.pack(side=tk.LEFT)
        self.entry2 = tk.Entry(self.rowframe2, width=40, textvariable=self.path2)
        self.entry2.pack(side=LEFT)

        self.rowframe3 = tk.Frame(self)
        self.rowframe3.pack(fill='x')
        self.btn3 = tk.Button(self.rowframe3, text='选择输出结果目录', width=12, command=self.btn3_click)
        self.btn3.pack(side=tk.LEFT)
        self.entry3 = tk.Entry(self.rowframe3, width=40, textvariable=self.path3)
        self.entry3.pack(side=LEFT)

        self.rowframe_result = tk.Frame(self)
        self.rowframe_result.pack(fill='x')
        self.text_result = tk.Text(self.rowframe_result, height=15, highlightbackground="black", wrap='none')
        self.text_result.pack()

        self.rowframe4 = tk.Frame(self)
        self.rowframe4.pack(fill='x')
        self.label = tk.Label(self.rowframe4, text="")
        self.label.pack(side=tk.LEFT)
        self.btn4 = tk.Button(self.rowframe4, bg="blue", fg="red", text="按这里执行对比", command=self.btn4_click)
        self.btn4.pack(side=tk.RIGHT)

        self.btn4_click()

    def btn0_click(self):
        dir_path = askdirectory()
        self.path0.set(dir_path)

    def btn1_click(self):
        dir_path = askdirectory()
        self.path1.set(dir_path)

    def btn2_click(self):
        dir_path = askdirectory()
        self.path2.set(dir_path)

    def btn3_click(self):
        dir_path = askdirectory()
        self.path3.set(dir_path)

    def click_handler(self):
        self.label.config(text="执行中...")
        self.label.config(bg="red")

        self.invalid_counter = 0
        self.total_counter = 0

        source_path0 = self.path0.get()
        source_path1 = self.path1.get()
        source_path2 = self.path2.get()
        dest_path = self.path3.get()

        for file_path in util.traverse_dir_iter(source_path0):
            file_path1 = file_path
            rel_path1 = util.get_rel_path(file_path1, source_path0)
            file_path2 = util.join_path(source_path1, rel_path1)
            # file_path2 = util.replace_dir_path(file_path, source_path1)

            if not self.result_path:
                self.result_path = util.get_result_dir(dest_path)
                util.clear_dir(self.result_path)

            comparator = JsonComparator(file_path1, file_path2)
            is_same, output_str = comparator.compare()

            # self.text_result.config(value=self.total_counter)

            self.total_counter = self.total_counter + 1
            if not is_same:
                print(file_path1)
                self.text_result.insert(END, output_str + '\n')

                self.invalid_counter = self.invalid_counter + 1
                orig_img_path = util.get_orig_image_file_path(source_path2, source_path0, file_path)
                # new_img_path = util.get_new_image_file_path(self.result_path, source_path0, file_path, orig_img_path)
                new_img_path = util.get_new_image_file_path(self.result_path, rel_path1, orig_img_path)

                util.ensure_dir(new_img_path)
                util.copy_file(orig_img_path, new_img_path)

                print(orig_img_path)
                print(new_img_path)
                print()

        self.label.config(text="执行完毕，共有 %s 张，有 %s 张有标注差异" % (self.total_counter, self.invalid_counter))
        self.label.config(bg="#00FF00")

    def btn4_click(self):
        self.t1 = threading.Thread(target=self.click_handler, args=())
        self.t1.start()

        # source_path0 = self.path0.get()
        # source_path1 = self.path1.get()
        # source_path2 = self.path2.get()
        # dest_path = self.path3.get()
        #
        # for file_path in util.traverse_dir_iter(source_path0):
        #     file_path1 = file_path
        #     file_path2 = util.replace_dir_path(file_path, source_path1)
        #
        #     if not self.result_path:
        #         self.result_path = util.get_result_dir(dest_path)
        #         util.clear_dir(self.result_path)
        #
        #     comparator = JsonComparator(file_path1, file_path2)
        #     is_same = comparator.compare()
        #
        #     if not is_same:
        #         # print('%s %s' % (is_same, file_path1))
        #         print(file_path1)
        #         orig_img_path = util.get_orig_image_file_path(source_path2, source_path0, file_path)
        #         new_img_path = util.get_new_image_file_path(self.result_path, source_path0, file_path, orig_img_path)
        #         util.ensure_dir(new_img_path)
        #         util.copy_file(orig_img_path, new_img_path)
        #         print(orig_img_path)
        #         print(new_img_path)
        #         print()

        # self.label.config(text="完毕！！")


if __name__ == '__main__':
    com = Comparator()
    com.mainloop()
    com.t1.join()
