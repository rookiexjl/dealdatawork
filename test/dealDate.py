# coding:utf-8
import os
import shutil
import datetime

'''
    项目:电信数据处理
    作者:xjl
    日期:20170515
'''

now = datetime.datetime.now()
now_date = now.strftime('%Y%m%d%H%M')


class DealDate:

    def __init__(self):

        self.deal1_dir = 'dir_first/'
        self.deal_set_file = 'dc/first_set/' + now_date + '.txt'

        self.deal2_dir_file_cm = 'dc/dir3c/cm.txt'
        self.deal2_dir_file_cu = 'dc/dir3c/cu.txt'
        self.deal2_dir_file_ct = 'dc/dir3c/ct.txt'

        self.deal3_dir1 = 'dc/dir3c/'

        self.deal_dir1 = 'dc/dir1/'

        self.deal_result_dir = 'dc/dirresult/'
        self.deal_result_not_found = 'dc/dirresult/notfound.csv'
        self.deal_scan = '/media/centos/snBase/'

        self.deal_scan_99 = '/media/centos/snBase/99.ot.txt'
        self.deal_result_renotfound = 'dc/dirresult/renotfound.csv'

        self.deal_new_result = 'dc/nresult/'
        self.match_dir = 'dc/match/'
        self.new_match_dir = 'dc/nmatch/'
        self.set_dir = 'dc/set/'
        self.result_dir = 'dc/result/'

    # 17319009913,10,中国电信,北京,北京,4.1
    # 去重通过电话号码18964656273和项目编号2.11
    def deal1(self):
        try:
            count = 0
            for parent, dirnames, filenames in os.walk(self.deal1_dir):
                for filename in filenames:
                    print filename
                    line_dict_uniq = dict()
                    with open(self.deal1_dir+filename, 'r') as fd:
                        for line in fd:
                            key = line.split(',')[0] + line.split(',')[5]
                            if key not in line_dict_uniq.keys():
                                line_dict_uniq[key] = line
                            else:
                                continue
                    for i in line_dict_uniq:
                        count += 1
                        line = line_dict_uniq[i]
                        with open(self.deal_set_file, "a") as f:
                            f.write(line)
            print '项目编号和号码去重后:' + str(count)
        except Exception, e:
            print Exception, ":", e
            print 'deal1 failure'
            os.remove(self.deal_set_file)

    # 区分运营商cm cu ct
    def deal2(self):
        try:
            count = 0
            fp = open(self.deal_set_file)
            for i in fp.readlines():
                line = i.split(',')[2].decode("gbk").encode("utf8")
                i = i.decode("gbk").encode("utf8")
                if line.find('中国移动') != -1:
                    count += 1
                    with open(self.deal2_dir_file_cm, "a") as f:
                        f.write(i)
                elif line.find('中国联通') != -1:
                    count += 1
                    with open(self.deal2_dir_file_cu, "a") as f:
                        f.write(i)
                elif line.find('中国电信') != -1:
                    count += 1
                    with open(self.deal2_dir_file_ct, "a") as f:
                        f.write(i)
                else:
                    with open(self.deal_result_not_found, "a") as f:
                        f.write(i)
            print '属于3大运营商有:' + str(count)
        except Exception, e:
            print Exception, ":", e
            print 'deal2 failure'
            os.remove(self.deal2_dir_file_cm)
            os.remove(self.deal2_dir_file_cu)
            os.remove(self.deal2_dir_file_ct)
            os.remove(self.deal_result_not_found)

    # 区分省份
    def deal3(self):
        try:
            province_dict = {"北京": "11", "天津": "12", "河北": "13",
                             "山西": "14", "内蒙古": "15", "辽宁": "21",
                             "吉林": "22", "黑龙江": "23", "上海": "31",
                             "江苏": "32", "浙江": "33", "安徽": "34",
                             "福建": "35", "江西": "36", "山东": "37",
                             "河南": "41", "湖北": "42", "湖南": "43",
                             "广东": "44", "广西": "45", "海南": "46",
                             "重庆": "50", "四川": "51", "贵州": "52",
                             "云南": "53", "西藏": "54", "陕西": "61",
                             "甘肃": "62", "青海": "63", "宁夏": "64",
                             "新疆": "65"}
            # 读取原数据生成对应省份的文件
            for parent, dirnames, filenames in os.walk(self.deal3_dir1):
                for filename in filenames:
                    fp = open(self.deal3_dir1 + filename)
                    for i in fp.readlines():
                        key = i.split(',')[3]
                        if key in province_dict:
                            with open(self.deal_dir1 + province_dict[key] + '.' + filename, "a") as f:
                                f.write(i)
                        else:
                            print '格式错误或者省份不对:' + i
                    fp.close()
        except Exception, e:
            print Exception, ":", e
            print 'deal4 failure'
            shutil.rmtree(self.deal_dir1)
            os.mkdir(self.deal_dir1)

    # 由于内存溢出取出分成2种方式
    def deal4(self):
        try:
            for parent, dirnames, filenames in os.walk(self.deal_dir1):
                for filename in filenames:
                    if filename == '32.cm.txt' or filename == '37.cm.txt' or filename == '44.cm.txt':
                        self.deal_big(filename)
                    else:
                        self.deal_min(filename)
        except Exception, e:
            print Exception, ":", e
            print 'deal5 failure'

    # 替换号码为编号
    # 17319009913 008030260
    # 17319009913,10,中国电信,北京,北京,4.1
    # 文件名为 4.1.11.ct.csv gbk格式
    # 008030260,2,中国电信,北京,北京
    def deal_min(self, filename):
        try:
            count = 0
            print "min filename is:" + filename
            fp1 = open(self.deal_scan + filename)
            d1 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
                  for k in fp1.readlines()}
            fp2 = open(self.deal_dir1 + filename)
            for j in fp2.readlines():
                if j.split(',')[0] in d1:
                    lines = j.replace(j.split(',')[0], d1.get(j.split(',')[0])).decode("utf8").encode("gbk")
                    count += 1
                    with open(self.deal_result_dir + filename.split('txt')[0] + 'csv', "a") as f:
                        f.write(lines)
                else:
                    with open(self.deal_result_not_found, "a") as f:
                        count += 1
                        f.write(j)
            print 'file_min_count:' + str(count)
            d1.clear()
            fp1.close()
            fp2.close()
        except Exception, e:
            print Exception, ":", e
            print 'dealMin failure:' + filename

    # 同上
    def deal_big(self, filename):
        try:
            count = 0
            print 'big filename is:' + filename
            file1 = self.deal_scan + filename
            file2 = self.deal_dir1 + filename
            file3 = self.deal_result_dir + filename.split('txt')[0] + 'csv'
            fp11 = open(file1)
            num = len(fp11.readlines())
            notfound1 = []
            notfound2 = []
            notfound3 = []
            fp1 = open(file1)
            fp2 = open(file2)
            if num <= 160000000:
                print '小于1.6e'
                d1 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
                      for k in fp1.readlines()[:80000000]}
                for j in fp2.readlines():
                    if j.split(',')[0] in d1:
                        lines = j.replace(j.split(',')[0], d1.get(j.split(',')[0])).decode("utf8").encode("gbk")
                        count += 1
                        with open(file3, "a") as f:
                            f.write(lines)
                    else:
                        notfound1.append(j)
                d1.clear()
                fp1.seek(0)
                fp2.seek(0)
                d2 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n") for k in
                      fp1.readlines()[80000000:]}
                for j in fp2.readlines():
                    if j.split(',')[0] in d2:
                        lines = j.replace(j.split(',')[0], d2.get(j.split(',')[0])).decode("utf8").encode("gbk")
                        count += 1
                        with open(file3, "a") as f:
                            f.write(lines)
                    else:
                        notfound2.append(j)
                fp1.close()
                fp2.close()
                d2.clear()
                for i in notfound1:
                    for j in notfound2:
                        if i == j:
                            count += 1
                            with open(self.deal_result_not_found, "a") as f:
                                f.write(j)
                print 'file_big_count:' + str(count)

            elif num <= 240000000:
                print '小于2.4e'
                d1 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
                      for k in fp1.readlines()[:80000000]}
                for j in fp2.readlines():
                    if j.split(',')[0] in d1:
                        lines = j.replace(j.split(',')[0], d1.get(j.split(',')[0])).decode("utf8").encode("gbk")
                        count += 1
                        with open(file3, "a") as f:
                            f.write(lines)
                    else:
                        notfound1.append(j)
                d1.clear()
                fp1.seek(0)
                fp2.seek(0)
                d2 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
                      for k in fp1.readlines()[80000000:160000000]}
                for j in fp2.readlines():
                    if j.split(',')[0] in d2:
                        lines = j.replace(j.split(',')[0], d2.get(j.split(',')[0])).decode("utf8").encode("gbk")
                        count += 1
                        with open(file3, "a") as f:
                            f.write(lines)
                    else:
                        notfound2.append(j)
                d2.clear()
                fp1.seek(0)
                fp2.seek(0)
                d3 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
                      for k in fp1.readlines()[160000000:]}
                for j in fp2.readlines():
                    if j.split(',')[0] in d3:
                        lines = j.replace(j.split(',')[0], d3.get(j.split(',')[0])).decode("utf8").encode("gbk")
                        count += 1
                        with open(file3, "a") as f:
                            f.write(lines)
                    else:
                        notfound3.append(j)
                d3.clear()
                fp1.close()
                fp2.close()
                for i in notfound1:
                    for j in notfound2:
                        if i == j:
                            for k in notfound3:
                                if i == k:
                                    count += 1
                                    with open(self.deal_result_not_found, "a") as f:
                                        f.write(j)

                print 'file_big_count:' + str(count)
        except Exception, e:
            print Exception, ":", e
            print 'dealBig failure:' + filename

    # 再次notfound.csv替换号码为编号通过99.ot.txt文件
    def deal_not_found(self):
        count = 0
        fp1 = open(self.deal_scan_99)
        d1 = {k.split(' ')[0]: k.split(' ')[1].split('\n')[0].strip("\n").strip("\r").strip("\n")
              for k in fp1.readlines()}
        fp2 = open(self.deal_result_not_found)
        for j in fp2.readlines():
            if j.split(',')[0] in d1:
                lines = j.replace(j.split(',')[0], d1.get(j.split(',')[0]))
                with open(self.deal_result_dir + '99.ot.csv', "a") as f:
                    f.write(lines.strip('\n').strip('\r').strip('\n') + ',' + j.split(',')[0] + '\n')
            else:
                with open(self.deal_result_renotfound, "a") as f:
                    count += 1
                    f.write(j)
        print 'allnotfound:' + str(count)
        d1.clear()
        fp1.close()
        fp2.close()
        os.remove(self.deal_result_not_found)

    # 区分为项目名
    def deal_result(self):
        count = 0
        for parent, dirnames, filenames in os.walk(self.deal_result_dir):
            for filename in filenames:
                file1 = self.deal_result_dir + filename
                file2 = self.deal_new_result + filename
                fp1 = open(file1)
                if filename == '99.ot.csv':
                    shutil.copy(file1, file2)
                elif filename == 'renotfound.csv':
                    shutil.copy(file1, file2)
                else:
                    for i in fp1:
                        file3 = self.deal_new_result + i.split(',')[5].strip('\n').strip('\r') + '.' + filename
                        count += 1
                        line = i.split(',')[0] + ',' + i.split(',')[1] + ',' + i.split(',')[2] + ',' +\
                            i.split(',')[3] + ',' + i.split(',')[4]
                        with open(file3, 'a') as f:
                            f.write(line + '\n')
        print '历史去重前所以项目和:' + str(count)

    # 历史去重
    def history_set_type(self):
        match1 = 'dc/match/pos.txt'
        match2 = 'dc/match/lty.txt'
        match3 = 'dc/match/dk.txt'
        match4 = 'dc/match/qhapp.txt'
        match5 = 'dc/match/tp.txt'
        match6 = 'dc/match/99.ot.csv'
        match7 = 'dc/match/renotfound.csv'
        match8 = 'dc/match/fcz.txt'
        path_list = [self.set_dir + now_date, self.result_dir + now_date]
        for path in path_list:
            if os.path.exists(path):
                pass
            else:
                os.mkdir(path)
        for parent, dirnames, filenames in os.walk(self.deal_new_result):
            for filename in filenames:
                if filename.split('.')[0] == '4':
                    match = match1
                    self.history_match_set(filename, match)
                elif filename.split('.')[0] == '6':
                    match = match2
                    self.history_match_set(filename, match)
                elif filename.split('.')[0] == '9':
                    match = match3
                    self.history_match_set(filename, match)
                elif filename.split('.')[0] == '28':
                    match = match4
                    self.history_match_set(filename, match)
                elif filename.split('.')[1] == 'ot':
                    fp1 = open(self.deal_new_result + filename)
                    fp2 = open(match6)
                    d1 = {k.split(',')[6].strip('\r').strip('\n').strip('\r') for k in fp2.readlines()}
                    for i in fp1.readlines():
                        line = i.split(',')[6].strip('\r').strip('\n')
                        if line in d1:
                            with open(self.set_dir + now_date + '/99.ot.csv', "a") as f:
                                f.write(i)
                        else:
                            with open(self.result_dir + now_date + '/' + filename, "a") as f:
                                f.write(i.decode('utf8').encode('gbk'))
                            with open(match6, "a") as f:
                                f.write(i.decode('utf8').encode('gbk'))
                elif filename.split('.')[0] == 'renotfound':
                    fp1 = open(self.deal_new_result + filename)
                    fp2 = open(match7)
                    d1 = {k.split(',')[0] for k in fp2.readlines()}
                    for i in fp1.readlines():
                        line = i.split(',')[0]
                        if line in d1:
                            with open(self.set_dir + now_date + '/renotfound.csv', "a") as f:
                                f.write(i)
                        else:
                            with open(self.result_dir + now_date + '/' + filename, "a") as f:
                                f.write(i.decode('utf8').encode('gbk'))
                            with open(match7, "a") as f:
                                f.write(i.decode('utf8').encode('gbk'))
                elif filename.split('.')[0] == '42':
                    match = match8
                    self.history_match_set(filename, match)
                else:
                    match = match5
                    self.history_match_set(filename, match)
        shutil.copytree(self.match_dir, self.new_match_dir + now_date)

    # 封装history_set方法
    def history_match_set(self, filename, match):
        file1 = self.set_dir + now_date + '/' + match.split('/')[-1]
        file2 = self.result_dir + now_date + '/' + filename
        file3 = match
        fp1 = open(self.deal_new_result + filename)
        fp2 = open(file3)
        d1 = {k.strip('\n').strip('\r') for k in fp2.readlines()}
        for i in fp1.readlines():
            line = i.split(',')[0] + i.split(',')[3] + filename.split('.')[-2]
            if line in d1:
                with open(file1, "a") as f:
                    f.write(i)
            else:
                with open(file2, "a") as f:
                    f.write(i)
                with open(file3, "a") as f:
                    f.write(line + '\n')


def main():
    DealDate().deal1()
    DealDate().deal2()
    DealDate().deal3()
    DealDate().deal4()
    DealDate().deal_not_found()
    DealDate().deal_result()
    DealDate().history_set_type()


if __name__ == '__main__':
    main()
