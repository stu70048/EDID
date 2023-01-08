#!/usr/bin/env python3 
import os, sys, re
import time
from argparse import ArgumentParser

def emtpybank(ROMtype ='flash') -> bytes:
    match ROMtype:
        case 'eeprom':
            bank_size = 256 #256 bytes
        case 'flash':
            bank_size = 64 * 1024 #64KB
    buffer =[0xff for i in range(bank_size)] # type: ignore
    return bytes(buffer)



def data2buffer(bin_list):
    buffer = bytes()
    for file in bin_list:
        print(file)
        with open(file, "rb") as f:
            buffer += f.read()
    return buffer

def write2bin(filename, write2buffer):
    newFileBytes = write2buffer
    with open(filename, "wb") as f:
        f.write(write2buffer)

    print("Done!")

def merge_bin(bin_list):
    buffer = data_to_buffer(bin_list)
    file_name = bin_list[0][:-4]
    write2bin(file_name, buffer)
    rename(file_name)
    
def simple_chks(file_name) -> str:
    big_bin_chks = 0
    with open(file_name, "rb") as f:
        data = f.read()
        for byte in data:
            big_bin_chks += byte
    return f'{big_bin_chks:>08X}'

def timestamp() -> str:
    timestamp = time.strftime("%Y%m%d_%H%M", time.localtime())
    return timestamp

def rename(file_name):
    new_name='{0}_{1}_{2}_color.bin'.format(file_name,simple_chks(file_name),timestamp()) #主名稱
    # enclosing inside try-except
    try:
        os.rename(file_name,new_name)
    except FileExistsError:
        print("File already Exists")
        print("Removing existing file")
        # skip the below code
        # if you don't' want to forcefully rename
        os.remove(new_name)
        # rename it
        os.rename(file_name, new_name)
        print('Done renaming a file')
    
if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8') 
    _OGC_BACKUP_BANK = 24
    _UC_BACKUP_BANK = 26
    parser = ArgumentParser()
    parser.add_argument('-sO', '--startOGC', help='OGC backup bank 位置', nargs='?', type=int, default=None)
    parser.add_argument('-sU', '--startUC', help='UC backup bank 位置', nargs='?', type=int, default=None)

    #args = parser.parse_args()
    args, unknownargs = parser.parse_known_args('1.bin -sO 25'.split())
    print(args,unknownargs)

    if args.startOGC:
        _OGC_BACKUP_BANK = args.startOGC
    if args.startUC:
        _UC_BACKUP_BANK = args.startUC


    if False:
        print('請使用以下格式!!')
        print('merge_bin.py <src_bin> <color_bin_1> [color_bin_n]')

    exit(0)
    print('--- use {0} seconds ---'.format(time.time() - start_time))
