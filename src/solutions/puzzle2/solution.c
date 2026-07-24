

int main(int argc, char* argv[])
{
    FILE *file = fopen("/home/joseph/repos/aoc-2025/tests/my_inputs/2.txt", "r");
    if (file == NULL) {
        perror("Error opening file");
        return 1;
    }
}