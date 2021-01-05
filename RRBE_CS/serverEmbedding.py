import numpy as np
from PIL import Image
from math import ceil
from Cryptodome.Cipher import AES
# from Crypto.Cipher import AES
from bitstring import BitArray


def pad(s):
    return (s + ((16 - len(s) % 16) * "{")).encode('utf-8')

def encrypt(cipher,plaintext):
    return cipher.encrypt(pad(plaintext))

def replace_lowbit(d, b):
    if d % 2 == b:
        return d
    elif d % 2 == 0:
        return d + 1
    else:
        return d - 1


def embeddingA(path=''):
    img = Image.open(path)
    matrix_input = np.asarray(img)
    matrix_input = matrix_input.astype(int)
    height, width = matrix_input.shape

    embedRate = 0.1

    max_data_length = embedRate * height * width


    A_height = ceil(max_data_length / width / 2)

    # handle embedding data
    data = '20174345qy'
    dataList = []
    # for i in data:
    #     tmp = bin(ord(i))[2:]
    #     for j in range(8-len(tmp)):
    #         dataList.append(0)
    #     for j in tmp:
    #         dataList.append(int(j))

    key = '20174355'
    cipher = AES.new(pad(key), AES.MODE_ECB)  # Adopt AES Encyption
    encrypted = encrypt(cipher, data)
    binary = BitArray(bytes=encrypted)
    s = [int(x) for x in binary.bin]  # Get binary list
    print(s)

    dataList += [1 for i in range(10)]
    dataList += [0 for i in range(10)]
    dataList = s+dataList
    
    if len(dataList) > max_data_length:
        print('embedding data too big.')
        return img
    

    # embedding
    num = 0
    for i in range(A_height):
        for j in range(width):
            num += 1

            if num <= 19:
                continue
            elif num == 20:
                matrix_input[i,j] = replace_lowbit(matrix_input[i,j], 1)
            elif num > len(dataList) + 20:
                break
            else:
                matrix_input[i,j] = replace_lowbit(matrix_input[i,j], dataList[num-21])
            
        if num > len(dataList) + 20:
            break
    

    #print("done")
    matrix_output = Image.fromarray(matrix_input).convert('L')
    matrix_output.save(path)


#embeddingA('H://专业综合设计//img//lenna_en.png',2)
    
