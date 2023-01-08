#!/usr/bin/env python3 
import re
import binascii
from os import listdir, makedirs
from os.path import getsize, exists
from time import time
import sys
from argparse import ArgumentParser


def bin2rtd(src_filepath, filename):
    start_time = time()
    filesize = getsize(src_filepath + filename)
    with open(src_filepath + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dst_path + filename[:-4] + '.rtd', 'wt') as f_rtd:
            f_point, hex_str = 0, ''
            for ch in data:
                if f_point % rtd_row_size == 0:
                    hex_str += whitespace * 4
                f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                if f_point % rtd_row_size != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    hex_str += whitespace
                else:
                    hex_str += '\n'
                    f_rtd.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2rtd use {1} seconds ---'.format(filename, time() - start_time))


def bin2ddc(src_filepath, filename):
    start_time = time()
    filesize = getsize(src_filepath + filename)
    with open(src_filepath + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dst_path + filename[:-4] + '.ddc', 'wt') as f_ddc:
            f_point, hex_str = 0, ''
            for ch in data:
                f_point, hex_str = f_point + 1, hex_str + f'{ch:0{2}X}'
                if f_point % ddc_row_size != 0 and f_point != filesize:
                    hex_str += whitespace
                else:
                    hex_str += '\n'
                    f_ddc.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2ddc use {1} seconds ---'.format(filename, time() - start_time))


def bin2txt(src_filepath, filename):
    start_time = time()
    filesize = getsize(src_filepath + filename)
    with open(src_filepath + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dst_path + filename[:-4] + '.txt', 'wt') as f_txt:
            f_point, hex_str = 0, ''
            for ch in data:
                if f_point % txt_row_size == 0:
                    hex_str += whitespace * 4
                f_point, hex_str = f_point + 1, hex_str + '0x' + f'{ch:0{2}X}' + ','
                if f_point % txt_row_size != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    hex_str += whitespace
                else:
                    hex_str = hex_str + whitespace + '\n'
                    f_txt.write(hex_str)
                    hex_str = ''
    print('--- {0} bin2txt use {1} seconds ---'.format(filename, time() - start_time))


def rtd2bin(src_filepath, filename):
    start_time = time()
    with open(src_filepath + filename, 'rt') as f_rtd:
        rtd_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_rtd.read()
        data = re.findall(rtd_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dst_path + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} rtd2bin use {1} seconds ---'.format(filename, time() - start_time))


def ddc2bin(src_filepath, filename):
    start_time = time()
    with open(src_filepath + filename, 'rt') as f_ddc:
        ddc_pattern = re.compile(r'[0-9a-fA-F]+')
        data = f_ddc.read()
        data = re.findall(ddc_pattern, data)
        data = ''.join(data)
        with open(dst_path + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} ddc2bin use {1} seconds ---'.format(filename, time() - start_time))


def txt2bin(src_filepath, filename):
    start_time = time()
    with open(src_filepath + filename, 'rt') as f_rtd:
        rtd_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_rtd.read()
        data = re.findall(rtd_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dst_path + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))
    print('--- {0} txt2bin use {1} seconds ---'.format(filename, time() - start_time))


def transfer2bin(src_filepath, filename , file_ext):
        match file_ext:
            case '.bin':
                pass
            case '.rtd':
                rtd2bin(src_filepath, filename)
            case '.ddc':
                ddc2bin(src_filepath, filename)
            case '.txt':
                txt2bin(src_filepath, filename)


def bin2other(src_filepath, filename):
    dst_file = dst_path + filename[:-4]
    if not exists(dst_file + '.rtd') and transfer2rtd:
        bin2rtd(src_filepath, filename)
    if not exists(dst_file + '.ddc') and transfer2ddc:
        bin2ddc(src_filepath, filename)
    if not exists(dst_file + '.txt') and transfer2txt:
        bin2txt(src_filepath, filename)


def main():
    if not exists(dst_path):
        makedirs(dst_path)
    dirs = listdir(src_path)
    for file in dirs:
        f_preix_name = file[:-4]  # 去掉副檔名
        f_ext = file[-4:].lower()  # 只產生小寫，如果來源的副檔名是大寫，在函數中會自動處理。
        if f_ext in file_extension:
            # 要用bin檔產生各ddc檔案，如果主bin檔不存在，自動生成bin檔並設置路徑。
            src_bin = f_preix_name + '.bin'
            if f_ext == '.bin':
                binpath = src_path
            else:
                binpath = dst_path
                if not exists(binpath + src_bin):
                    transfer2bin(src_path, file, f_ext)
            bin2other(binpath, src_bin)
    print("done!!")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', help='設定輸出資料夾, ex: ./output/', action='store_true')
    parser.add_argument('-r', '--rtd', help='轉換rtd檔', action='store_true')
    parser.add_argument('-d', '--ddc', help='轉換ddc檔', action='store_true')
    parser.add_argument('-t', '--txt', help='轉換txt檔', action='store_true')
    parser.add_argument('-a', '--all', help='轉換所有ddc檔', action='store_true')
    parser.add_argument("-rn", '--rtd_row_size', help="設定rtd一行有幾個數字", nargs='?', type=int, default=16)
    parser.add_argument("-dn", '--ddc_row_size', help="設定rtd一行有幾個數字", nargs='?', type=int, default=8)
    parser.add_argument("-tn", '--txt_row_size', help="設定rtd一行有幾個數字", nargs='?', type=int, default=16)
    args = parser.parse_args()

    # global const
    file_extension = ['.bin', '.rtd', '.ddc', '.txt']
    whitespace = ' '
    src_path = './'

    if args.output:
        dst_path = './'
    else:
        dst_path = './output/'

    transfer2rtd = args.all or args.rtd or True
    transfer2ddc = args.all or args.ddc
    transfer2txt = args.all or args.txt

    rtd_row_size = args.rtd_row_size
    ddc_row_size = args.ddc_row_size
    txt_row_size = args.txt_row_size

    main()