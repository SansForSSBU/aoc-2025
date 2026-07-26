#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef enum {
    UNKNOWN = -1,
    LEFT,
    RIGHT
} Direction;

typedef struct {
    Direction dir;
    int clicks;
} Instruction;

Direction to_direction (char c)
{
    if (c == 'L')
    {
        return LEFT;
    }
    else if (c == 'R')
    {
        return RIGHT;
    }
    return UNKNOWN;
}

Instruction parse_instruction(char* line)
{
    Direction dir = to_direction(line[0]);
    int clicks;
    int items_read = sscanf(&line[1], "%d", &clicks);
    Instruction ret = {dir, clicks};
    return ret;
}

typedef struct {
    int pt1_ans;
    int pt2_ans;
} Answers;

Answers solve_problem(FILE *file)
{
    int dial = 50;
    int pt1_ans = 0;
    int pt2_ans = 0;

    char buffer[256];
    while (fgets(buffer, sizeof(buffer), file) != NULL)
    {
        Instruction i = parse_instruction(buffer);
        int clicks = i.clicks;
        Direction dir = i.dir;
        int clicks_to_zero;
        if (dir == LEFT)
        {
            clicks_to_zero = dial;
            dial = (((dial-clicks) % 100)+100) % 100;
        }
        else
        {
            clicks_to_zero = 100-dial;
            dial = (((dial+clicks) % 100)+100) % 100;
        }
        if (clicks_to_zero == 0)
        {
            clicks_to_zero = 100;
        }
        if (clicks >= clicks_to_zero)
        {
            pt2_ans += 1;
            int remaining = clicks - clicks_to_zero;
            pt2_ans += remaining / 100;
        }
        if (dial == 0)
        {
            pt1_ans += 1;
        }
    }
    Answers ret = {pt1_ans, pt2_ans};
    return ret;
}

int main(int argc, char* argv[])
{
    FILE *file = fopen("../../../inputs/1.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    Answers ans = solve_problem(file);
    printf("Part 1 ans: %d\n", ans.pt1_ans);
    printf("Part 2 ans: %d\n", ans.pt2_ans);
    fclose(file);
    return 0;
}