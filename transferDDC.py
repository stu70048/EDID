# uncompyle6 version 3.8.0
# Python bytecode 3.5.2 (3351)
# Decompiled from: Python 3.5.4 (v3.5.4:3f56838, Aug  8 2017, 02:17:05) [MSC v.1900 64 bit (AMD64)]
# Embedded file name: transferDDC.py
# Compiled at: 2017-02-13 22:42:20
# Size of source mod 2**32: 272 bytes
import os, sys, array
path = '.'
dirs = os.listdir(path)

def ddc2rtd


def rtd2bin


def bin2rtd


def bin2ddc


dirs = os.listdir(path)
file_type = 0
for file in dirs:
    if file[-4:] == '.ddc' or file[-4:] == '.DDC':
        file_type = 0
    else:
        if file[-4:] == '.rtd' or file[-4:] == '.RTD':
            file_type = 1
        elif file[-4:] == '.bin' or file[-4:] == '.BIN':
            file_type = 2

if file_type == 0:
    for file in dirs:
        print(file)
        ddc2rtd(file)

    dirs = os.listdir(path)
    for file in dirs:
        print(file)
        rtd2bin(file)

else:
    if file_type == 1:
        for file in dirs:
            print(file)
            rtd2bin(file)

        dirs = os.listdir(path)
        for file in dirs:
            print(file)
            bin2ddc(file)

    elif file_type == 2:
        for file in dirs:
            bin2rtd(file)

        dirs = os.listdir(path)
        for file in dirs:
            print(file)
            bin2ddc(file)