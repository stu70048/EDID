/* ========================================================================== */
/*                                                                            */
/*   Filename.c                                                               */
/*   (c) 2012 Author                                                          */
/*                                                                            */
/*   Description                                                              */
/*                                                                            */
/* ========================================================================== */
#include <stdio.h>                                                                                 

int main(int argc, char* argv[])
{
    FILE *fp;
    int c, sum;
    
    fp = fopen(argv[1],"rb");
    if (fp == NULL) {
        printf("FFFF");
        return(-1);
    }

    sum = 0;
    while ((c = fgetc(fp)) != EOF) {
        sum += c;
    }

    printf("%04X", sum & 0xFFFF);
    
    fclose(fp);
    
    return 0;
}
