# coding:utf-8
import os

dir_name = '3/'


def countLineForDir(dir_name):
    count = 0
    for parent, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            fp1 = open(parent + '/' + filename)
            for i in fp1:
                if i.strip() != '':
                    print i
                    count += 1
    print count

countLineForDir(dir_name)