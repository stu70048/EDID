chcp 65001
cd /d %cd%
set file1=BenQ_PD2706U_20221125_PVT
::set file2=BenQ_PD2706UA
python ./mergeBin.py %file1%.bin  -b 24 ./sunny_OGC_bank59_n.bin ./sunny_OGC_bank60_n.bin ./Bank61_UC_n.bin
::python ./colordata/merge_bin.py %file2%.bin ./colordata/bank.bin ./colordata/sunny_OGC_bank59_n.bin ./colordata/sunny_OGC_bank60_n.bin ./colordata/Bank61_UC_n.bin
::python ./colordata/merge_bin.py BenQ_PD2706U_20221109_V1_PVT.bin ./colordata/bank.bin ./colordata/sunny_OGC_bank59_n.bin ./colordata/sunny_OGC_bank60_n.bin ./colordata/Bank61_UC_n.bin
::python ./colordata/merge_bin.py BenQ_PD2706U_20221109_V2_PVT.bin ./colordata/bank.bin ./colordata/sunny_OGC_bank59_n.bin ./colordata/sunny_OGC_bank60_n.bin ./colordata/Bank61_UC_n.bin
pause