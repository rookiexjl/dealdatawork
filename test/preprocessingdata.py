# coding:utf-8
import os
import datetime

now = datetime.datetime.now()
now_date = now.strftime('%Y%m%d%H%M')
numAreaBd_file = 'numAreaBd20170511.csv'
matchNumAreaBd_file = 'mergefile/' + now_date + '.txt'


class PreDate():

    def __init__(self):
        self.dealDate_dir = '0511/'

        self.matchNumAreaBd_file1 = 'mergefile/' + now_date + '_7.csv'
        self.matchNumAreaBd_file2 = 'mergefile/' + now_date + '_notfound7.csv'

    def dealDate(self):
        count = 0
        list1 = []
        for parent, dirnames, filenames in os.walk(self.dealDate_dir):
            for filename in filenames:
                path = self.dealDate_dir + filename
                fpfile = open(path)
                for i in fpfile:
                    count += 1
                    lines = i.split('\t')[0] + ',' + i.split('\t')[2].split('P')[1] + ',' + i.split('\t')[4]
                    list1.append(lines)
                fpfile.close()
        print 'all_summary_date_count:' + str(count)
        return list1

    # 读取sdate目录下所有文件，匹配numAreaBd.csv文件并拼接地址
    # 然后输入到ndate目录下生成对应的文件
    def matchNumAreaBd(self, list_date):
        count = 0
        fp1 = open(numAreaBd_file)
        d1 = {k.split(',')[0]: k.split(',')[3].strip('\r').strip('\n') + ',' + k.split(',')[1] + ',' +
              k.split(',')[2] for k in fp1.readlines()}
        list1 = []
        for line in list_date:
            if line.split(',')[0].strip()[:7] in d1:
                with open(matchNumAreaBd_file, "a") as f:
                    f.write(line.split(',')[0] + ',' + line.split(',')[2] + ',' +
                            d1.get(line.split(',')[0][:7]) + ',' + line.split(',')[1] + '\n')
            else:
                count += 1
                list1.append(line.split(',')[0][:7])
                line1 = line + ',中国未知,未知,未知' + '\n'
                with open(self.matchNumAreaBd_file1, "a") as f:
                    f.write(line1)
        list2 = set(list1)
        for i in list2:
            with open(self.matchNumAreaBd_file2, "a") as f:
                f.write(i + '\n')
        print 'not_found_7num_count:' + str(count)
        fp1.close()


def main():
    list = PreDate().dealDate()
    PreDate().matchNumAreaBd(list)


if __name__ == '__main__':
    main()

