#!/usr/bin/env python3 
import os, sys
import time
from argparse import ArgumentParser
class MergeBin():
    def __init__(self, bankSize):
        self.bankSize = bankSize
        self.defaultBank =[0xff for i in range(self.bankSize)]
        self.buffer = bytes()

    def getNumBanks(self) -> int:
        retval = int(len(self.buffer)/self.bankSize)
        return retval
        
    def addDefaultBank(self):
        self.buffer += bytes(self.defaultBank)
        
    def add(self, file):
        with open(file, "rb") as f:
            self.buffer += f.read()
        
    def extractBank(self, index):
        self.buffer = self.buffer[(index*bankSize):((index+1)*bankSize)]
        
    def save(self, fileName):
        with open(fileName, "wb") as f:
            f.write(self.buffer)
    
def simpleChecksum(data) -> str:
    chks = 0
    for val in data:
        chks += val 
    return f'{chks:>08X}'

def timestamp() -> str:
    timestamp = time.strftime("%Y%m%d_%H%M", time.localtime())
    return timestamp

if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8') # type: ignore
    _NAME = str()
    _OGC_BACKUP_BANK = int()
    parser = ArgumentParser()
    parser.add_argument('-b', '--bank', help='OGC backup bank(.h)', nargs='?', type=int, default=None)
    parser.add_argument('-e', '--extract', help='extract target bank', nargs='?', type=int, default=None)
    parser.add_argument('-o', '--output', help='binName', nargs='?', type=str, default=None)
    args, filelist = parser.parse_known_args()
    #print(filelist)
    if not args.bank:
        print('[WARING]PLEASE SET BANK NUMBER')
    else:
        _OGC_BACKUP_BANK = args.bank
        
    if len(filelist) < 2 and not args.extract:
        print('請使用以下格式!!')
        print('mergeBin.py <src_bin> -b _BACKUP_BANK <color_bin_0> [color_bin_n]')
    else:
        # main
        bankSize = 64*1024 #64KB
        merge = MergeBin(bankSize)
        merge.add(filelist[0])
        mainBinName = filelist[0][:-4]
        del filelist[0]
        # 
        if args.extract:
            merge.extractBank(args.extract)
        else:
            if args.bank:
                while(merge.getNumBanks() < _OGC_BACKUP_BANK):
                    merge.addDefaultBank()
                    
            for i in filelist:
                merge.add(i)
        
        if args.output:
            _NAME = args.output
        elif args.extract:
            _NAME = '{0}_bank{1}.bin'.format(mainBinName, args.extract)
        else:
            _NAME = '{0}_{1}_{2}.bin'.format(mainBinName, simpleChecksum(merge.buffer), timestamp())

        if os.path.exists(_NAME):
            os.remove(_NAME)
            
        merge.save(_NAME)   
        print("Done!")
