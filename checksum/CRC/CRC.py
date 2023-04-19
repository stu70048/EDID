from time import time
class CRC():
    def __init__(self):
        self.gCrc=0

    def ProcessCRC (self, data):
        for byte in data:
            self.gCrc ^= byte<<8
            for i in range(8):
                if self.gCrc & 0x8000:
                    self.gCrc ^= 0x1070<<3
                self.gCrc <<= 1

    def GetCRC(self):
        return ( self.gCrc >>8 ) & 0xFF

def fileCRC (filename,bankSize):
    with open(filename, 'rb') as f:
        content=f.read()
        crc = CRC()
        addr = 0
        while addr < len(content):
            
            buf = content[slice (addr, addr+bankSize)]
            crc.ProcessCRC(buf)
            
            data_crc = crc.GetCRC()
            
            print (f"bank {int(addr/bankSize):0{2}d} CRC is  {data_crc:0{2}X}")
            addr += bankSize
            crc.gCrc=0

    return data_crc
bankSize = 64 * 1024 #64KB
filename="BenQ_PD2706U_EVT2_0DB14441_20221221.bin"
buffer =[0xff for i in range(bankSize*2)] # type: ignore
start_time = time()
#fileCRC(bytes(buffer),bankSize)
fileCRC(filename,bankSize)
print('--- use {0} seconds ---'.format(time() - start_time))
