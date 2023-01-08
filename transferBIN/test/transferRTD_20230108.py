#!/usr/bin/env python3 
from os import listdir, makedirs
from os.path import exists
import sys
from argparse import ArgumentParser

def main():
    src = src_path
    dst = dst_path
    if not exists(dst):
        makedirs(dst)
    dirs = listdir(src)
    for file in dirs:
        f_preix_name = file[:-4]  # 去掉副檔名
        f_ext = file[-4:].lower()  # 只產生小寫，如果來源的副檔名是大寫，在函數中會自動處理。
        if f_ext in file_extension:
            # 要用bin檔產生各ddc檔案，如果主bin檔不存在，自動生成bin檔並設置路徑。
            src_bin = f_preix_name + '.bin'
            if f_ext == '.bin':
                binpath = src
            else:
                binpath = dst
                if not exists(binpath + src_bin):
                    transfer2bin(file, src, dst, f_ext)
            bin2other(src_bin, binpath, dst, file_extension, file_row_size)
    print("done!!")


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    from lib_transfer import bin2other,transfer2bin
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
    transfer2rtd = args.all or args.rtd or True
    transfer2ddc = args.all or args.ddc
    transfer2txt = args.all or args.txt
    
    rtd_row_size = args.rtd_row_size
    ddc_row_size = args.ddc_row_size
    txt_row_size = args.txt_row_size
    
    file_extension = {'.bin':None, '.rtd':transfer2rtd, '.ddc':transfer2ddc, '.txt':transfer2txt}
    file_row_size = {'.rtd':rtd_row_size, '.ddc':ddc_row_size, '.txt':txt_row_size}
    whitespace = ' '
    src_path = './'

    if args.output:
        dst_path = './'
    else:
        dst_path = './output/'

    main()