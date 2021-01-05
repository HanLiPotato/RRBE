import sys
sys.path.append(r'C:/Users/10712/Desktop/FTP-master/RRBE_CS')
from RRBE_op import *
import os
import numpy
from PIL import Image
from math import ceil,floor
import traceback2 as traceback

from Cryptodome.Cipher import AES
# from Crypto.Cipher import AES
from bitstring import BitArray


def AESdecrypt(cipher,encrypted):
    dec = str(cipher.decrypt(encrypted))
    padding = dec.count('{')
    return dec[2:len(dec)-padding-1]
def pad(s):
    return (s + ((16 - len(s) % 16) * "{")).encode('utf-8')



def RRBE_upload(path='', embedRate=0.1,cipher='test'):
    if not os.path.exists(path):
        raise Exception('文件不存在，请重新选择')

    sourceDir,filename =os.path.dirname(path), os.path.basename(path).split('.')[0]
    extendName = os.path.basename(path).split('.')[-1]
    dstfilePath = sourceDir+'//'+filename+'_en'+'.png'
    #dstfilePath = sourceDir+'//'+filename+'_en'+'.'+extendName


    img = Image.open(path)
    img = trans_to_GreyScale(img)
    width, height = img.size
    max_data_length = embedRate * height * width

    A_height = ceil(max_data_length / width / 2)
    A, B, index = divide_img(img, A_height)


    dataList = np.asarray(A)
    dataList = dataList.astype(int)
    matrixA = dataList.copy()
    dataList %= 2
    dataList = list(dataList.flat)

    
    
    # Embedding LSB info from A to B.
    embeddingRound = 1
    print("Embedding round:", embeddingRound)
    handled_matrixB = embedB(B, dataList, index)

    print("Embedding done.")

    # concat & encrypt
    handled_matrixB_copy = handled_matrixB.copy()
    handled_img = np.concatenate((matrixA, handled_matrixB))
    encrypted_img = encrypt(handled_img, cipher)

    image_output = Image.fromarray(encrypted_img).convert('L')
    image_output.save(dstfilePath)#如果有同名文件未处理
    image_output.close()
    return dstfilePath



def RRBE_extract(path='',embedRate=0.1,key='1234'):
    if not os.path.exists(path):
        raise Exception('文件不存在')



    img = Image.open(path)
    matrix_input = np.asarray(img)
    matrix_input = matrix_input.astype(int)
    height, width = matrix_input.shape
    max_data_length = embedRate * height * width

    #Get part A and B.

    A_height = ceil(max_data_length / width / 2)

    matrix_input_copy = list(matrix_input.copy().flat)  
    startFlag = [1 for i in range(15)]
    A_pos = -1

    for i in range(0,len(matrix_input_copy),width):
        tmpFlag = matrix_input_copy[i:i+15]
        tmpFlag = [x%2 for x in tmpFlag]
        if tmpFlag == startFlag:
            A_pos = i // width
            break
    
    if A_pos < 0:
        raise Exception('非可提取图片')

    data = matrix_input[A_pos:A_pos+A_height,:] % 2
    endFlag = [1 for i in range(10)]
    endFlag += [0 for i in range(10)]
    data = list(data.flat)

    if data[19] != 1:
        raise Exception('图片未嵌入信息')
    
    endIndex = -1
    for i in range(20,len(data)):
        if data[i:i+20] == endFlag:
            endIndex = i
    
    if endIndex < 0:
        raise Exception('嵌入信息无结束标志位，提取失败')
    data = data[20:endIndex] if endIndex > 0 else data[20:]

    # message = ''
    # for i in range(0,len(data),8):
    #     tmp = data[i:i+8]
    #     tmp = ''.join([str(x) for x in tmp])
    #     message += chr(int(tmp,2))


    datalist = [str(x) for x in data]
    #print(datalist)
    cipher = AES.new(pad(key), AES.MODE_ECB)
    byts = BitArray(bin=''.join(datalist))
    message = AESdecrypt(cipher, byts.bytes)

    return message


def RRBE_decrypt(path='',embedRate=0.1,cipher='test'):
    if not os.path.exists(path):
        raise Exception('文件不存在')

    sourceDir, filename = os.path.dirname(path), os.path.basename(path).split('.')[0]
    dstfilePath = sourceDir + '//' + filename + '_de' + '.png'


    img = Image.open(path)
    matrix_input = np.asarray(img)
    matrix_input = matrix_input.astype(int)
    height, width = matrix_input.shape
    max_data_length = embedRate * height * width

    #Get part A and B.
    A_height = ceil(max_data_length / width / 2)

    decrypted_img = decrypt(matrix_input, cipher, A_height)

    image_output = Image.fromarray(decrypted_img).convert('L')
    image_output.save(dstfilePath)



def RRBE_recovery(path='',embedRate=0.1):
    if not os.path.exists(path):
        raise Exception('文件不存在')

    sourceDir, filename = os.path.dirname(path), os.path.basename(path).split('.')[0]
    dstfilePath = sourceDir + '//' + filename + '_re' + '.png'


    img = Image.open(path)
    matrix_input = np.asarray(img)
    matrix_input = matrix_input.astype(int)
    height, width = matrix_input.shape
    max_data_length = embedRate * height * width

    #Get part A and B.


    A_height = ceil(max_data_length / width / 2)

    recoveryed_img= recoveryAB(matrix_input, A_height)
    image_output = Image.fromarray(recoveryed_img).convert('L')
    image_output.save(dstfilePath)


def checkerror(path1,path2):
    img1 = Image.open(path1)
    img1 = trans_to_GreyScale(img1)
    matrix_input1 = np.asarray(img1)
    matrix_input1 = matrix_input1.astype(int)

    img2 = Image.open(path2)
    matrix_input2 = np.asarray(img2)
    matrix_input2 = matrix_input2.astype(int)

    if list(matrix_input1.flat) == list(matrix_input2.flat):
        print('YES')
    else:
        print('No')
        # print(list(matrix_input1.flat))
        # print('\n\n\n\n')
        # print(list(matrix_input2.flat))


