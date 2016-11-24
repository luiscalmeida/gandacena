#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <./hivex-1.3.13/lib/hivex.h>

void extractOS(const char *filename){
    hivex_h *hive = hivex_open(filename, 0);
}
