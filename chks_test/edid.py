import crcmod

#from PyCRC.CRC16 import CRC16
#from PyCRC.CRC16DNP import CRC16DNP
#from PyCRC.CRC16Kermit import CRC16Kermit
#from PyCRC.CRC16SICK import CRC16SICK
#from PyCRC.CRC32 import CRC32
#from PyCRC.CRCCCITT import CRCCCITT

#input = '12345'
#print(CRCCCITT().calculate(input))
CHUNK_HEADER_SIZE = 0x80                      # The size of chunk header is 128 bytes.
BOOTLOADER_SIZE   = 0						  # The size of sboot+chunk_header_size = 64K*n bytes.
CHUNK_HEADER_BASE = 0				       	  # chunk_header_base is at the end of sboot
UNCOMPRESSED_LEN  = 0x3800                    # The size of uncompressed part is 14K bytes.

bLittleEndian = False
bCRC16Enable  = True
bMultiFlash   = False
PM_CODE_SIZE  = 0             # The size of PM code is supposed to be passed by argument.
AP_BASE       = 0             # AP base is at the end of sboot+chunk_header+PM
UNCOMP_LEN    = 0             # Uncompressed length of AP.bin

#$(BinIDPackFiles) -BIGENDIAN -CRC16ENABLE -multiflash 8 8 0958336900 
#$@ $(BIN_INFO) $(IMGINFO_OFFSET) $(APC_BIN) 0 $(OS_TYPE) 
#$(PM_BIN_SIZE) $(SBOOT_BIN_SIZE) $(UNCOMP_LEN) $(ENABLE_USB_HOST_DUAL_IMAGE_OFFSET)

#python scripts/BinIDPackFiles_Compress.py -BIGENDIAN -CRC16ENABLE -multiflash 8 8 0958336900 
# Bin_MST9U3_EX240N/MERGE.bin ././monitor_ap/CUSTOM/BENQ_EX/BININFO/BinInfo.h 4352 .//Bin_MST9U3_EX240N/AP_C.bin 0 nos_aeon 
# 65536 65536 $((0x00003800)) 0x100000
IMGINFO_OFFSET = 4352
PM_BIN_SIZE =65536
SBOOT_BIN_SIZE=65536
UNCOMP_LEN=0x00003800
ENABLE_USB_HOST_DUAL_IMAGE_OFFSET=0x100000

CHUNK_HEADER_BASE = BOOTLOADER_SIZE
PM_CODE_SIZE=PM_BIN_SIZE
AP_BASE         = BOOTLOADER_SIZE + CHUNK_HEADER_SIZE + PM_CODE_SIZE
#crc = struct.pack('>L', CRC32(f_res.read()))

CRC16 = crcmod.mkCrcFun(0x18005, 0, 0)
CRC32 = crcmod.mkCrcFun(0x104C11DB7, 0, 0)
f_elf = open("AP_C.bin", 'r+b', 0)
data = f_elf.read()
data2=f_elf.tell()
print(hex(CRC16(data)))
print(hex(CRC32(data)))
print(hex(data2))
f_bin = open("MERGE_after.bin", 'r+b', 0)
f_bin.seek(AP_BASE)
data4 = f_bin.read(data2)

#print(hex(data4))
print(hex(CRC16(data4)))
print(hex(CRC32(data4)))
f_bin.seek(0)
print(hex(f_bin.tell()))
#print(CRC16().calculate(data))
#print(CRC16DNP().calculate(data))
#print(CRC16Kermit().calculate(data))
#print(CRC16SICK().calculate(data))
#print(CRC32().calculate(data))
#print(CRCCCITT().calculate(data))

f_elf.close()
f_bin.close()