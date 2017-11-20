/* Check how arrays are represented in the program. */

void function()
{
    int arrayOnStack[5];
    int* arrayInHeap = new int[5];
    while(true);
}

int main(void)
{
    function();
    return 0;
}