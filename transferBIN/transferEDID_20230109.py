#!/usr/bin/env python3 
import re, sys ,binascii
from os import listdir, makedirs
from os.path import getsize, exists
from time import time
from argparse import ArgumentParser
# need python version > 3.10
def bin2rtd(filename, src, dest, f_ext, rowLen):
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + f_ext, 'wt') as f_rtd:
            f_point, str = 0, ''
            for ch in data:
                #-------------------------------------------------------------------------------------------
                if f_point % rowLen == 0:
                    str += whitespace * 4
                #-------------------------------------------------------------------------------------------
                f_point, str = f_point + 1, str + '0x' + f'{ch:0{2}X}' + ','
                #-------------------------------------------------------------------------------------------
                if f_point % rowLen != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    str += whitespace
                else:
                    str += '\n'
                    f_rtd.write(str)
                    str = ''
                
def bin2ddc(filename, src, dest, f_ext, rowLen):
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + f_ext, 'wt') as f_ddc:
            f_point, str = 0, ''
            for ch in data:
                #-------------------------------------------------------------------------------------------
                # ddc無空白
                #-------------------------------------------------------------------------------------------
                f_point, str = f_point + 1, str + f'{ch:0{2}X}'
                #-------------------------------------------------------------------------------------------
                if f_point % rowLen != 0 and f_point != filesize:
                    str += whitespace
                else:
                    str += '\n'
                    f_ddc.write(str)
                    str = ''
                
def bin2txt(filename, src, dest, f_ext, rowLen):
    filesize = getsize(src + filename)
    with open(src + filename, 'rb') as f_bin:
        data = f_bin.read()
        with open(dest + filename[:-4] + f_ext, 'wt') as f_txt:
            f_point, str = 0, ''
            for ch in data:
                #-------------------------------------------------------------------------------------------
                if f_point % rowLen == 0:
                    str += whitespace * 4
                #-------------------------------------------------------------------------------------------
                f_point, str = f_point + 1, str + '0x' + f'{ch:0{2}X}' + ','
                #-------------------------------------------------------------------------------------------
                if f_point % rowLen != 0 and f_point != filesize:  # 如果還沒寫滿一行數量或讀完data，填補空格。
                    str += whitespace
                else:
                    str = str + whitespace + '\n'
                    f_txt.write(str)
                    str = ''
                
def rtd2bin(filename, src, dest):
    with open(src + filename, 'rt') as f_rtd:
        rtd_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_rtd.read()
        data = re.findall(rtd_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))

def ddc2bin(filename, src, dest):
    with open(src + filename, 'rt') as f_ddc:
        ddc_pattern = re.compile(r'[0-9a-fA-F]+')
        data = f_ddc.read()
        data = re.findall(ddc_pattern, data)
        data = ''.join(data)
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))

def txt2bin(filename, src, dest):
    with open(src + filename, 'rt') as f_txt:
        txt_pattern = re.compile(r'0x[0-9a-fA-F]+,')
        data = f_txt.read()
        data = re.findall(txt_pattern, data)
        data = ''.join(data).replace('0x', '').replace(',', '')
        with open(dest + filename[:-4] + '.bin', 'wb') as f_bin:
            f_bin.write(binascii.unhexlify(data))

def xxx2bin(filename, src, dest, f_ext):
    start_time = time()
    match f_ext:
        case '.bin':
            pass
        case '.rtd':
            rtd2bin(filename, src, dest)
        case '.ddc':
            ddc2bin(filename, src, dest)
        case '.txt':
            txt2bin(filename, src, dest)
    print('--- {0} {1}2bin use {2} seconds ---'.format(filename, f_ext[-3:], time() - start_time))
    
def bin2xxx(filename, src, dest, f_ext, ext_rowLen):
    start_time = time()
    match f_ext:
        case '.rtd':
            bin2rtd(filename, src, dest, f_ext, ext_rowLen[f_ext])
        case '.ddc':
            bin2ddc(filename, src, dest, f_ext, ext_rowLen[f_ext])
        case '.txt':
            bin2txt(filename, src, dest, f_ext, ext_rowLen[f_ext])
    print('--- {0} bin2{1} use {2} seconds ---'.format(filename, f_ext[-3:], time() - start_time))

# 要用bin檔產生各ddc檔案，如果主bin檔不存在，自動生成bin檔並設置路徑。
def main():
    # 來源與生成路徑配置
    src = src_path      
    dest = dest_path    
    if not exists(dest):
        makedirs(dest)
    dirs = listdir(src)
    
    for file in dirs:
        f_preix_name = file[:-4]  # 去掉副檔名
        f_ext = file[-4:].lower()  # 只產生小寫，如果來源的副檔名是大寫，在函數中會自動處理。
        src_bin = f_preix_name + '.bin'
        if f_ext == '.bin' or f_ext in file_extension_support:
            match f_ext:
                case '.bin':
                    binpath = src
                case _:
                    binpath = dest
                    if not exists(binpath + src_bin):
                        xxx2bin(file, src, dest, f_ext)
        #--------------------------------------------------------------------------
            for ext in file_extension_support: # support list
                if file_extension_support[ext]:
                    if not exists(dest + f_preix_name + ext):
                        bin2xxx(src_bin, binpath, dest, ext, file_rowLen)
                    else:
                       # print('{0} is aleady exit'.format(f_preix_name + ext))
                        pass
    print("done!!")

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    parser = ArgumentParser()
    parser.add_argument('-o', '--output', help='設定輸出資料夾, ex: ./output/', action='store_true')
    parser.add_argument('-r', '--rtd', help='轉換rtd檔', action='store_true')
    parser.add_argument('-d', '--ddc', help='轉換ddc檔', action='store_true')
    parser.add_argument('-t', '--txt', help='轉換txt檔', action='store_true')
    parser.add_argument('-a', '--all', help='轉換所有ddc檔', action='store_true')
    parser.add_argument("-rn", '--rtd_rowLen', help='設定rtd一行有幾個數字', nargs='?', type=int, default=16)
    parser.add_argument("-dn", '--ddc_rowLen', help='設定ddc一行有幾個數字', nargs='?', type=int, default= 8)
    parser.add_argument("-tn", '--txt_rowLen', help='設定txt一行有幾個數字', nargs='?', type=int, default=16)
    args = parser.parse_args()

    # global const---------------------------------------------------------------------------
    support2rtd = args.all or args.rtd or True
    support2ddc = args.all or args.ddc or True
    support2txt = args.all or args.txt
    
    rtd_rowLen = args.rtd_rowLen
    ddc_rowLen = args.ddc_rowLen
    txt_rowLen = args.txt_rowLen
    
    file_extension_support = {'.rtd': support2rtd, '.ddc': support2ddc, '.txt': support2txt}
    file_rowLen = {'.rtd': rtd_rowLen, '.ddc': ddc_rowLen, '.txt': txt_rowLen}
    whitespace = ' '
    src_path = './'
    #----------------------------------------------------------------------------------------
    if args.output: # or True:
        dest_path = './output/'
    else:
        dest_path = './'
        
    main()