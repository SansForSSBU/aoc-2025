#include <stdio.h>
#include <string.h>
#include <malloc.h>

typedef struct Range {
    char* num1;
    char* num2;
} Range;

typedef struct Node {
    struct Range* range;
    struct Node* next;
} Node;

Range* create_range(const char* n1, const char* n2) {
    Range* r = (Range*)malloc(sizeof(Range));
    if (r == NULL) return NULL;

    r->num1 = strdup(n1);
    r->num2 = strdup(n2);

    return r;
}

void free_range(Range* r) {
    free(r->num1);
    free(r->num2);
    free(r);
}

int main(int argc, char* argv[])
{
    FILE *file = fopen("../../../inputs/2.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    char buffer[512];
    fgets(buffer, sizeof(buffer), file);
    char *saveptr1, *saveptr2;
    char* token = strtok_r(buffer, ",", &saveptr1);
    while (token != NULL) {
        char* num1 = strtok_r(token, "-", &saveptr2);
        char* num2 = strtok_r(NULL, "-", &saveptr2);
        Range* r = create_range(num1, num2);
    }
    return 0;
}