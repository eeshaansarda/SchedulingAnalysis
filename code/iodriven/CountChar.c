#include <stdlib.h>
#include <stdio.h>
#include <dirent.h>
#include <errno.h>
#include <string.h>

int countCharInFile(FILE *f) {
    int count = 0;
    char ch;

    while ((ch = fgetc(f)) != EOF){
        count++;
    }

    return count;
}

int countChar(char* dirname) {
    int count = 0;
    struct dirent *d;
    DIR *dh = opendir(dirname);
    FILE *f;

    if (!dh) {
        if (errno = ENOENT)
        {
            //If the directory is not found
            perror("Directory doesn't exist");
        }
        else
        {
            //If the directory is not readable then throw error and exit
            perror("Unable to read directory");
        }
        exit(EXIT_FAILURE);
    }
    while ((d = readdir(dh)) != NULL) {
        //If hidden files are found we continue
        if(d->d_name[0] == '.') continue;

        char temp[80], fdname[80] = "./text/";
        strcpy(temp, d->d_name);
        strcat(fdname, temp);
        f = fopen(fdname, "r");
        count += countCharInFile(f);
    }
    return count;
}


int main() {
    // printf("%i", countChar("./text"));
    FILE *f;
    for(int i = 0; i < 4000; i++) {
        f = fopen("./iodriven/text/1.txt", "r");
        countCharInFile(f);
        fclose(f);
    }
}
