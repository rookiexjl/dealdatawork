# coding:utf-8
import os
import sys
import re
import xlrd
import shutil
from des1 import DES

def renamePid(PidFile, result, notfound):

    CT_Table = 'cttable.xlsx'
    for parent, dirnames, filenames in os.walk(PidFile):
        for filename in filenames:

            table = xlrd.open_workbook(CT_Table).sheet_by_name(u'Sheet1')
            nrows = table.nrows
            d1 = {table.row_values(i)[1].split('P')[1]: table.row_values(i)[9]
                  for i in range(1, nrows)}

            if re.findall(r'\d+.\d+', filename):
                name = re.findall(r'\d+.\d+', filename)[0]
                name1 = filename.split(re.findall(r'\d+.\d+', filename)[0])[1]                
                if d1.has_key(name):
                    not_file = d1.get(name).encode("gbk")
                    if os.path.exists(result+not_file):
                        shutil.copy(PidFile + filename, result + not_file + '/' + not_file + name1)
                    else:
                        os.mkdir(result+not_file)
                        shutil.copy(PidFile + filename, result + not_file + '/' + not_file + name1)
                else:
                    print name

            elif filename.find('renotfound.csv') != -1:
                fp1 = open(PidFile+filename)
                for line in fp1:
                    line = line.strip('\n').strip('\r').strip('\n')
                    lineList = line.split(",")

                    number = lineList[0]
                    desNumber = DES().desencode(number, "x3y9i0g@")
                    name = lineList[-1]

                    if d1.has_key(name):
                        not_file = d1.get(name).encode("gbk")
                        notfound_dir = notfound + not_file
                        notfound_file = notfound + not_file+'/'+not_file+'.enc.csv'
                        nline = line.replace(number, desNumber) + '\n'
                        if os.path.exists(notfound_dir):
                            with open(notfound_file, 'a') as f:
                                f.write(nline)
                        else:
                            os.mkdir(notfound_dir)
                            with open(notfound_file, 'a') as f:
                                f.write(nline)
                    else:
                        print name

            elif filename.find('99.ot') != -1:
                print PidFile + filename
                print result
                shutil.copy(PidFile + filename, result)


def countLineForDir(dir_name):
    count = 0
    for parent, dirnames, filenames in os.walk(dir_name):
        for filename in filenames:
            fp1 = open(parent + '/' + filename)
            for i in fp1:
                if i.strip() != '':
                    count += 1
    return str(count)


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print 'Error:please input cmd as "python xxx.py pidFile/"'
        quit

    PidFile = sys.argv[1]
    result = 'result/' + PidFile.split('/')[-2] + '/'
    notfound = 'notfound/' + PidFile.split('/')[-2] + '/'

    print 'filename:' + result

    if os.path.exists(result) and os.path.exists(notfound):
        renamePid(PidFile, result, notfound)
    else:
        path_list =[result, notfound]
        for path in path_list:
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)
        renamePid(PidFile, result, notfound)
    print '去重后匹配项目号码数量:' + countLineForDir(result)
    print '没有发现:' + countLineForDir(notfound)
    histroysetpath = 'dc/set/' + PidFile.split('/')[-2]
    print '历史去重' + countLineForDir(histroysetpath)
