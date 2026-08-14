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

typedef struct Node {
    struct Range* range;
    struct Node* next;
} Node;

Range* create_range(const int n1, const int n2) {
    Range* r = (Range*)malloc(sizeof(Range));
    if (r == NULL) return NULL;

    r->num1 = n1;
    r->num2 = n2;

    return r;
}

void free_range(Range* r) {
    free(r);
}

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

int main(int argc, char* argv[])
{
    FILE *file = fopen("../../../inputs/2.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    char buffer[512] = {0};
    fgets(buffer, sizeof(buffer), file);
    char *saveptr1, *saveptr2;
    char* token = strtok_r(buffer, ",", &saveptr1);
    while (token != NULL) {
        char* num1 = strtok_r(token, "-", &saveptr2);
        char* num2 = strtok_r(NULL, "-", &saveptr2);
        int start;
        int end;
        Range* r;
        if (safe_str_to_int(num1, &start) && safe_str_to_int(num2, &end))
        {
            r = create_range(start, end);
            printf("%d-%d\n", r->num1, r->num2);
        }
        token = strtok_r(NULL, ",", &saveptr1);
    }
    return 0;
}