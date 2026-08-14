#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <malloc.h>
#include <limits.h>
#include <errno.h>
#include <stdbool.h>

typedef struct Range {
    int num1;
    int num2;
} Range;

bool safe_str_to_int(const char* str, int* out)
{
    if (str == NULL || *str == '\0') {
        return false;
    }

    char* endptr = NULL;
    errno = 0;

    long val = strtol(str, &endptr, 10);

    if (errno == ERANGE) {
        return false;
    }

    if (*endptr != '\0') {
        return false;
    }

    if (val < INT_MIN || val > INT_MAX) {
        return false;
    }

    *out = (int)val;
    return true;
}

bool parse_input(char* input, Range* ranges, int* num_ranges)
{
    char *saveptr1, *saveptr2;
    char* token = strtok_r(input, ",", &saveptr1);
    while (token != NULL) {
        char* num1 = strtok_r(token, "-", &saveptr2);
        char* num2 = strtok_r(NULL, "-", &saveptr2);
        int start;
        int end;
        if (safe_str_to_int(num1, &start) && safe_str_to_int(num2, &end))
        {
            Range r = {start, end};
            ranges[(*num_ranges)++] = r;
        }
        else
        {
            return false;
        }
        token = strtok_r(NULL, ",", &saveptr1);
    }
    return true;
}

int main(int argc, char* argv[])
{
    FILE *file = fopen("../../../inputs/2.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    char buffer[512] = {0};
    Range ranges[64] = {0};
    int num_ranges = 0;
    fgets(buffer, sizeof(buffer), file);
    parse_input(buffer, ranges, &num_ranges);
    
    return 0;
}