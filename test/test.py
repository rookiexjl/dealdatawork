
fp1 = open('1/cm.txt')
for i in fp1.readlines()[2:]:
    print i.split(',')[0]
fp1.seek(0)
for j in fp1:
    print j.split(',')[3].decode('gbk')
fp1.close()

# with open('1/cm.txt', 'rb') as f:
#    for i in f:
#       print i
#
#    f.seek(0)
#    for j in f:
#       print j

