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
#include <inttypes.h>

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

bool parse_input(char* input, Range* ranges, uint64_t* num_ranges)
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

uint64_t positive_integer_power_of_ten(uint64_t power)
{
    uint64_t ret = 1;
    for (uint64_t i = 0; i < power; i++)
    {
        ret = ret * 10;
    }
    return ret;
}

uint64_t repeat_num_n_times(uint64_t num, int num_times)
{
    int num_digits = count_digits(num);
    uint64_t ret = num;
    for (int i = 1; i < num_times; i++)
    {
        ret += num * positive_integer_power_of_ten(i * num_digits);
    }
    return ret;
}

uint64_t get_invalid_at_idx_pt1(uint64_t idx)
{
    return repeat_num_n_times(idx, 2);
}

void get_invalids_at_idx_pt2(uint64_t idx, uint64_t* buff, uint64_t* num_returned)
{
    uint64_t max_len = 14;
    uint64_t length = count_digits(idx);
    num_returned = 0;
    for (uint64_t num_repeats = 2; num_repeats <= max_len / length; num_repeats++)
    {
        buff[(*num_returned)++] = repeat_num_n_times(idx, num_repeats);
    }
}

void add_invalid_to_ans_if_in_ranges(uint64_t invalid, uint64_t* ans, Range* ranges, uint64_t num_ranges)
{
    for (uint64_t i = 0; i < num_ranges; i++)
    {
        Range r = ranges[i];
        if (invalid >= r.num1 && invalid <= r.num2)
        {
            (*ans) += invalid;
        }
    }
}

uint64_t solve_pt1(Range* ranges, uint64_t num_ranges)
{
    uint64_t pt1_ans = 0;
    uint64_t max_len = 14;
    for (uint64_t i = 1; i < positive_integer_power_of_ten(max_len / 2); i++)
    {
        uint64_t num = get_invalid_at_idx_pt1(i);
        add_invalid_to_ans_if_in_ranges(num, &pt1_ans, ranges, num_ranges);
    }
    return pt1_ans;
}

uint64_t solve_pt2(Range* ranges, uint64_t num_ranges)
{
    uint64_t pt2_ans = 0;
    uint64_t max_len = 14;
    uint64_t buff[14] = {0};
    uint64_t num_returned = 0;
    for (uint64_t i = 1; i < positive_integer_power_of_ten(max_len / 2); i++)
    {
        get_invalids_at_idx_pt2(i, buff, &num_returned);
        for (uint64_t v = 0; v < num_returned; v++)
        {
            uint64_t num = buff[v];
            add_invalid_to_ans_if_in_ranges(num, &pt2_ans, ranges, num_ranges);
        }
    }
    return pt2_ans;
}

int main()
{
    FILE *file = fopen("../../../inputs/2.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    char buffer[512] = {0};
    Range ranges[64] = {0};
    uint64_t num_ranges = 0;
    char* ret = fgets(buffer, sizeof(buffer), file);
    if (ret == NULL)
    {
        return 1;
    }
    if (parse_input(buffer, ranges, &num_ranges) == false)
    {
        return 1;
    }
    uint64_t pt1_ans = solve_pt1(ranges, num_ranges);
    printf("Part 1 ans: %" PRIu64 "\n", pt1_ans);

    uint64_t pt2_ans = solve_pt2(ranges, num_ranges);
    printf("Part 2 ans: %" PRIu64 "\n", pt2_ans);
    return 0;
}