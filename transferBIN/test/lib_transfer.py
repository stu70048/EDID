#!/usr/bin/env python3 
import re
import binascii
from os import listdir, makedirs
from os.path import getsize, exists
from time import time
import sys
from argparse import ArgumentParser

whitespace = ' '
def bin2rtd(filename, src, dest, row_size):
    start_time = time()
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + '.rtd', 'wt') as f_rtd:
            f_point, hex_str = 0, ''
            for ch in data:
                if f_point % row_size == 0:
                    hex_str += whitespace * 4
                f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                if f_point % row_size != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    hex_str += whitespace
                else:
                    hex_str += '\n'
                    f_rtd.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2rtd use {1} seconds ---'.format(filename, time() - start_time))


def bin2ddc(filename, src, dest, row_size):
    start_time = time()
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + '.ddc', 'wt') as f_ddc:
            f_point, hex_str = 0, ''
            for ch in data:
                f_point, hex_str = f_point + 1, hex_str + f'{ch:0{2}X}'
                if f_point % row_size != 0 and f_point != filesize:
                    hex_str += whitespace
                else:
                    hex_str += '\n'
                    f_ddc.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2ddc use {1} seconds ---'.format(filename, time() - start_time))


def bin2txt(filename, src, dest, row_size):
    start_time = time()
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + '.txt', 'wt') as f_txt:
            f_point, hex_str = 0, ''
            for ch in data:
                if f_point % row_size == 0:
                    hex_str += whitespace * 4
                f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                if f_point % row_size != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    hex_str += whitespace
                else:
                    hex_str = hex_str + whitespace + '\n'
                    f_txt.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2txt use {1} seconds ---'.format(filename, time() - start_time))


def rtd2bin(filename, src, dest):
    start_time = time()
    with open(src + filename, 'rt') as f_rtd:
        rtd_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_rtd.read()
        data = re.findall(rtd_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} rtd2bin use {1} seconds ---'.format(filename, time() - start_time))


def ddc2bin(filename, src, dest):
    start_time = time()
    with open(src + filename, 'rt') as f_ddc:
        ddc_pattern = re.compile(r'[0-9a-fA-F]+')
        data = f_ddc.read()
        data = re.findall(ddc_pattern, data)
        data = ''.join(data)
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} ddc2bin use {1} seconds ---'.format(filename, time() - start_time))


def txt2bin(filename, src, dest):
    start_time = time()
    with open(src + filename, 'rt') as f_rtd:
        rtd_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_rtd.read()
        data = re.findall(rtd_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} txt2bin use {1} seconds ---'.format(filename, time() - start_time))


def transfer2bin(filename, src, dest, file_ext):
        match file_ext:
            case '.bin':
                pass
            case '.rtd':
                rtd2bin(filename, src, dest)
            case '.ddc':
                ddc2bin(filename, src, dest)
            case '.txt':
                txt2bin(filename, src, dest)


def bin2other(filename, src, dest, ext_dict, row_size_dict):
    dst_file = dest + filename[:-4]
    for f_ext in row_size_dict:
        if not exists(dst_file + f_ext) and ext_dict[f_ext]:
            bin2xxx(filename, src, dest, f_ext, row_size_dict[f_ext])

        
def bin2xxx(filename, src, dest , f_ext, row_size):
    start_time = time()
    dst_file = dest + filename[:-4]
    if not exists(dst_file + f_ext):
        filesize = getsize(src + filename)
        with open(src + filename, 'rb') as f_bin:
            data = f_bin.read()
            with open(dst_file + f_ext, 'wt') as f_xxx:
                f_point, hex_str = 0, ''
                for ch in data:
                    #--------------------------------------
                    if f_point % row_size == 0:
                        match f_ext:
                            case '.rtd':
                                hex_str += whitespace * 4
                            case '.ddc':
                                pass
                            case '.txt':
                                hex_str += whitespace * 4
                    #--------------------------------------
                    match f_ext:
                        case '.rtd':
                            f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                        case '.ddc':
                            f_point, hex_str = f_point + 1, hex_str + f'{ch:0{2}X}'
                        case '.txt':
                            f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                    #--------------------------------------
                    if f_point % row_size != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                        hex_str += whitespace
                    else:
                        match f_ext:
                            case '.rtd':
                                hex_str += '\n'
                            case '.ddc':
                                hex_str += '\n'
                            case '.txt':
                                hex_str = hex_str + whitespace + '\n'
                        f_xxx.write(hex_str)
                        hex_str = ''
                    #--------------------------------------
        print('--- {0} bin2{1} use {2} seconds ---'.format(filename, f_ext[-3:], time() - start_time))
    else:
        print('{0} file is already exist',format(dst_file + f_ext))
