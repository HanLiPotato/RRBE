
# def b():
#     raise Exception('Exception in b')
#
# def test():
#     b()
#     raise Exception('yi')
#
# try:
#     test()
# except Exception as e:
#     print(str(e))
#
# import os
# path = 'c://Users//ASUS//Desktop//origin.jpg'
# filename = path.split('//')[-1].split('.')[0]
# pwd = str(path.split('//')[0:-1])
# print(pwd)
# sourceDir,filename =os.path.dirname(path), os.path.basename(path).split('.')[0]
# dstfilePath = sourceDir+'//'+filename+'en'+'.png'
# print(dstfilePath)
a=[9,10]
b=[7,8,9]
c=[]
c = a+c
c=b+c


print(c)
print(a)