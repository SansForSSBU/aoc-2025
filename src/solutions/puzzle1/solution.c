#include <stdio.h>
#include <stdlib.h>
#include <sys/queue.h>
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

struct node {
    Instruction data;
    TAILQ_ENTRY(node) entries;
};

TAILQ_HEAD(queue_head, node);


struct queue_head parse_input(FILE *file)
{
    struct queue_head my_queue;
    TAILQ_INIT(&my_queue);
    char buffer[256];
    while (fgets(buffer, sizeof(buffer), file) != NULL)
    {
        Instruction i = parse_instruction(buffer);
        struct node *n1 = malloc(sizeof(struct node));
        n1->data = i;
        TAILQ_INSERT_TAIL(&my_queue, n1, entries);
    }
    return my_queue;
}

int solve_pt1(struct queue_head instructions)
{
    int dial = 50;
    int clicks = 0;
    struct node *item;
    TAILQ_FOREACH(item, &instructions, entries) {
        if (item->data.dir == LEFT)
        {
            dial = (dial - item->data.clicks) % 100;
        }
        else
        {
            dial = (dial + item->data.clicks) % 100;
        }
        if (dial == 0)
        {
            clicks += 1;
        }
    }
    return clicks;
}

int main(int argc, char* argv[])
{
    FILE *file = fopen("/home/joseph/repos/aoc-2025/tests/my_inputs/1.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    struct queue_head instructions = parse_input(file);

    struct node *item;

    int pt1_ans = solve_pt1(instructions);
    printf("Part 1 ans: %d\n", pt1_ans);

    fclose(file);
    return 0;
}