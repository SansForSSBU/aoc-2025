#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <ctype.h>
#include <string.h>
#include <malloc.h>
#include <limits.h>
#include <errno.h>
#include <stdbool.h>
#include <math.h>

typedef struct Range {
    uint64_t num1;
    uint64_t num2;
} Range;

char* trim(char* str)
{
    if (str == NULL) return NULL;

    while (isspace((unsigned char)*str)) {
        str++;
    }

    if (*str == '\0') {
        return str;
    }

    char *end = str + strlen(str) - 1;

    while (end > str && isspace((unsigned char)*end)) {
        end--;
    }
    *(end+1) = '\0';

    return str;
}

bool safe_str_to_uint64(char* str, uint64_t* out)
{
    if (str == NULL || *str == '\0') {
        return false;
    }

    char* endptr = NULL;
    errno = 0;
    str = trim(str);

    unsigned long long val = strtoull(str, &endptr, 10);

    if (errno == ERANGE) {
        return false;
    }

    if (*endptr != '\0') {
        return false;
    }

    if (val > UINT64_MAX) {
        return false;
    }

    *out = (uint64_t)val;
    return true;
}

int count_digits(uint64_t n)
{
    int count = 0;
    do {
        count++;
        n /= 10;
    } while (n != 0);

    return count;
}

bool parse_input(char* input, Range* ranges, int* num_ranges)
{
    char *saveptr1, *saveptr2;
    char* token = strtok_r(input, ",", &saveptr1);
    while (token != NULL) {
        char* num1 = strtok_r(token, "-", &saveptr2);
        char* num2 = strtok_r(NULL, "-", &saveptr2);
        uint64_t start;
        uint64_t end;
        if (safe_str_to_uint64(num1, &start) && safe_str_to_uint64(num2, &end))
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

uint64_t positive_integer_power_of_ten(int power)
{
    uint64_t ret = 1;
    for (int i = 0; i < power; i++)
    {
        ret = ret * 10;
    }
    return ret;
}

bool make_invalids_with_n_digits(uint64_t* buffer, int* count, int num_digits)
{
    if (num_digits % 2 != 0)
    {
        return false; // Odd numbers are not supported.
    }
    if (num_digits > 18)
    {
        return false; // uint64_t cannot store numbers this large
    }
    for (int i = positive_integer_power_of_ten((num_digits / 2)-1); i < positive_integer_power_of_ten(num_digits / 2); i++)
    {
        uint64_t num = i * positive_integer_power_of_ten(num_digits / 2) + i;
        buffer[(*count)++] = num;
    }
    return true;
}

uint64_t solve_pt1(Range* ranges, int num_ranges)
{
    for (int i = 0; i < num_ranges; i++)
    {
        Range r = ranges[i];
        int num_digits = count_digits(r.num2);
        int buff_len = positive_integer_power_of_ten(num_digits / 2) - positive_integer_power_of_ten((num_digits / 2) - 1);
        uint64_t* buffer = malloc(sizeof(uint64_t) * buff_len);
        int num_invalids = 0;
        make_invalids_with_n_digits(buffer, &num_invalids, num_digits);
        printf("%d", num_invalids);
    }
    return 0;
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
    if (parse_input(buffer, ranges, &num_ranges) == false)
    {
        return 1;
    }
    uint64_t pt1_ans = solve_pt1(ranges, num_ranges);
    return 0;
}