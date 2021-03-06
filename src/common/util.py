#!/usr/bin/python
# -*- coding: UTF-8 -*-

import os
import json
import glob

from shutil import copyfile, rmtree


def traverse_dir_iter(file_path):
    """
    递归遍历目录，迭代器
    :param file_path:
    :return:
    """
    files = os.listdir(file_path)
    for fi in files:
        fi_d = os.path.join(file_path, fi)
        if os.path.isdir(fi_d):
            yield from traverse_dir_iter(fi_d)
        else:
            tmp = os.path.join(file_path, fi_d)
            yield tmp
            # yield os.path.join(file_path, fi_d)
            # print(os.path.join(file_path, fi_d))


def join_path(path1, path2):
    return os.path.join(path1, path2)


def get_rel_path(path, start):
    rel_path = os.path.relpath(path, start)
    return rel_path


def replace_dir_path(file_path, dir_path):
    # sub_path = os.path.relpath(file_path, dir_path)

    _, file_name = os.path.split(file_path)
    # _, filename = os.path.split(filepath_2)
    new_dir = os.path.join(dir_path, file_name)
    # print(new_dir)
    return new_dir


def ensure_dir(path):
    path = os.path.dirname(path)
    if not os.path.exists(path):
        # path = os.path.dirname(path)
        os.makedirs(path)


def copy_file(src_path, dest_path):
    try:
        copyfile(src_path, dest_path)
    except:
        print('file %s not exist' % src_path)


def clear_dir(path):
    if os.path.exists(path):
        rmtree(path)


def get_file_name_from_path(path):
    return os.path.basename(path)


def get_result_dir(root_path):
    img_sub_dir_name = 'result'
    return os.path.join(root_path, img_sub_dir_name)


def get_new_image_file_path(result_dir, rel_path, orig_path):
    path = os.path.join(result_dir, rel_path)
    path_pre, _ = os.path.splitext(path)
    _, suffix = os.path.splitext(orig_path)
    path = path_pre + suffix
    return path


def get_new_image_file_path2(result_dir, json_dir_path, json_file_path, orig_path):
    sub_path = os.path.relpath(json_file_path, json_dir_path)
    sub_path_text, file_extension = os.path.splitext(sub_path)
    # img_sub_dir_name = 'result'
    # new_img_dir_name = os.path.join(root_path, img_sub_dir_name)

    # # 先删除存放结果的文件夹
    # if os.path.exists(new_img_dir_name):
    #     rmtree(new_img_dir_name)
    _, suffix = os.path.splitext(orig_path)
    img_path = os.path.join(result_dir, sub_path_text + suffix)
    return img_path


def get_orig_image_file_path(root_path, json_dir_path, json_file_path):
    try:
        sub_path = os.path.relpath(json_file_path, json_dir_path)
        sub_path_text, file_extension = os.path.splitext(sub_path)
        # img_path = os.path.join(root_path, sub_path_text + '.*')

        img_path_pre = os.path.join(root_path, sub_path_text)
        img_path_pre = glob.escape(img_path_pre)
        img_path = img_path_pre + '.*'

        li = glob.glob(img_path)

        return li[0]
    except:
        return None


def file2json(file_path):
    """
    读取文件，并将文件转成json
    :param file_path:
    :return:
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_item = json.load(f)
        return json_item


if __name__ == '__main__':
    path = get_new_image_file_path('/Users/bitsonli/Desktop/projects/',
                                   '/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果1',
                                   '/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果1/336-1-28.json',
                                   'png')
    path = get_orig_image_file_path('/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/图片',
                                    '/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果1',
                                    '/Users/bitsonli/Desktop/projects/data/脱发分类试标结果/结果1/336-1-28.json')
    print(path)
