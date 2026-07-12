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

typedef struct {
    int pt1_ans;
    int pt2_ans;
} Answers;

Answers solve_problem(struct queue_head instructions)
{
    int dial = 50;
    int pt1_ans = 0;
    int pt2_ans = 0;
    struct node *item;
    TAILQ_FOREACH(item, &instructions, entries) {
        for (int i=0; i<item->data.clicks; i++)
        {
            if (item->data.dir == LEFT)
            {
                dial = (dial - 1) % 100;
            }
            else
            {
                dial = (dial + 1) % 100;
            }
            if (dial == 0) {
                pt2_ans += 1;
            }
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
    FILE *file = fopen("/home/joseph/repos/aoc-2025/tests/my_inputs/1.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
    struct queue_head instructions = parse_input(file);

    struct node *item;

    Answers ans = solve_problem(instructions);
    printf("Part 1 ans: %d\n", ans.pt1_ans);
    printf("Part 2 ans: %d\n", ans.pt2_ans);
    fclose(file);
    return 0;
}