#!/usr/bin/python
# -*- coding: UTF-8 -*-

from src.common.util import file2json


class Comparator(object):
    def __init__(self, item1, item2):
        self.item1 = item1
        self.item2 = item2

    def compare(self):
        pass


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

            if not json1['labeled'] or not json2['labeled']:
                return False

            size1 = json1['size']
            size2 = json2['size']
            if size1['width'] == 574:
                pass

            if abs(size1['width'] - size2['width']) > self.width_threshold:
                return False

            if abs(size1['height'] - size2['height']) > self.height_threshold:
                return False

            if abs(size1['depth'] - size2['depth']) > self.depth_threshold:
                return False

            return True
        except:
            raise Exception()
            return False
