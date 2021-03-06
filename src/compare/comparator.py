#!/usr/bin/python
# -*- coding: UTF-8 -*-

from src.common.util import file2json, get_file_name_from_path


class Comparator(object):
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2

    def compare(self):
        pass


class Extractor(object):
    def __init__(self, file):
        self.file = file


class SexExtractor(Extractor):

    def __init__(self, file):
        super().__init__(file)

    def extract(self):
        try:
            json1 = file2json(self.file)

            '''
            1. labeled指示图片是否有标记过（即true），必须标记过才继续下面的逻辑，否则不通过
            2. 假如labeled都为true，则检查outputs.object[0].name属性，男的话返回male，女的话返回female

            {
              "path": "E:\\中山艾里斯传媒\\2018.12.15\\一二三四周\\新建文件夹\\13岁\\13UJpsb.jpg",
              "outputs": {
                "object": [
                  {
                    "name": "女"
                  }
                ]
              },
              "time_labeled": 1545012223199,
              "labeled": true,
              "size": {
                "width": 341,
                "height": 322,
                "depth": 3
              }
            }
            '''

            output_str = ''
            if not json1['labeled']:
                filename = get_file_name_from_path(self.file)
                output_str = '文件 %s -----> labeled 的值是 %s' % (filename, json1['labeled'])
                print('labeled1 %s' % json1['labeled'])
                return None, output_str

            if json1['outputs']['object'][0]['name'] == '男':
                return 'male', None
            elif json1['outputs']['object'][0]['name'] == '女':
                return 'female', None
        except Exception as ex:
            print('file %s excetion raised' % self.file)
            return None, None


class JsonComparator(Comparator):

    def __init__(self, file1, file2):
        super().__init__(file1, file2)

        self.width_threshold = 2
        self.height_threshold = 2
        self.depth_threshold = 2

    def compare(self):
        try:
            json1 = file2json(self.item1)
            json2 = file2json(self.item2)

            '''
            1. labeled指示图片是否有标记过（即true），必须标记过才继续下面的逻辑，否则不通过
            2. 假如labeled都为true，则比较outputs.object[0].name属性，相同即一样，不一样则不通过
            
            {
              "path": "E:\\试标\\试标\\005-1-45.jpg",
              "outputs": {
                "object": [
                  {
                    "name": "发际线高"
                  }
                ]
              },
              "time_labeled": 1543386712281,
              "labeled": true,
              "size": {
                "width": 586,
                "height": 759,
                "depth": 3
              }
            }
            '''
            output_str = ''
            if not json1['labeled'] or not json2['labeled']:
                filename = get_file_name_from_path(self.item1)
                output_str = '文件 %s -----> labeled1 %s, labeled2 %s' % (filename, json1['labeled'], json2['labeled'])
                print('labeled1 %s, labeled2 %s' % (json1['labeled'], json2['labeled']))
                return False, output_str

            if json1['outputs']['object'][0]['name'] != json2['outputs']['object'][0]['name']:
                filename = get_file_name_from_path(self.item1)
                output_str = '文件 %s -----> name1 %s, name2 %s' % (
                    filename, json1['outputs']['object'][0]['name'], json2['outputs']['object'][0]['name'])
                print('json1 name %s, json2 name %s' % (
                    json1['outputs']['object'][0]['name'], json2['outputs']['object'][0]['name']))
                return False, output_str

            return True, ''
        except Exception as ex:
            print('file %s excetion raised' % self.item1)
