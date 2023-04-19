#include <stdio.h>
#include <stdlib.h>
#include <string.h>
# include<time.h>
/* run this program using the console pauser or add your own getch, system("pause") or input loop */
unsigned char GetCRC( unsigned char *data, int len);
unsigned int  GetFileSize(FILE* fp) ;
int main(int argc, char *argv[]) {
	int banksize=64*1024;
	unsigned int FileSize=0;
	unsigned int offset=0;
	unsigned char buffer[banksize];
	
	clock_t start, end;
	double execution_time;
	start = clock();
	
	FILE *fp = fopen("BenQ_PD2706U_EVT2_0DB14441_20221221.bin","rb");
	FileSize=GetFileSize(fp);
	while(FileSize>=banksize){
		fseek(fp, offset, SEEK_SET);
		fread(&buffer, sizeof(unsigned char), banksize, fp);
		//memcpy(buffer, fp, banksize);
		//printf("%s\n", &buffer);
		printf("bank %2d CRC is %02X\n",offset/banksize,GetCRC(buffer,banksize));
		offset+=banksize;
		FileSize-=banksize;
		//fseek(fp, offset, SEEK_SET);
		//fseek(fp, banksize, SEEK_CUR);
	}
	fclose(fp);
	end = clock();
	execution_time = ((double)(end - start))/CLOCKS_PER_SEC;
	printf("Time taken to execute in seconds : %f", execution_time);

	return 0;
}
unsigned char BankCRC(unsigned char *data)
{
	unsigned int banksize = 64*1024;
	return GetCRC(data,banksize);
}

unsigned char GetCRC( unsigned char *data, int len)
{
	
	unsigned int gCrc = 0;
	int i, j;
	for (j = len; j; j--, data++) {
		gCrc ^= (*data << 8);
		for(i = 8; i; i--) {
			if (gCrc & 0x8000)
				gCrc ^= (0x1070 << 3);
			gCrc <<= 1;
		}
	}
	return (unsigned char)(gCrc >> 8);
}

unsigned int  GetFileSize(FILE* fp) {
	unsigned int FileSize=0;
  fseek(fp, 0L, SEEK_END);
  FileSize = ftell(fp);
	//fseek(fp, 0L, SEEK_SET);
	rewind(fp);
  return FileSize;
}