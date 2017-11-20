/* Check how arrays are represented in the program. */

void function()
{
    int arrayOnStack[5];

    /* Not even the mighty GDB can understand that this particular int * is part of a
       group of 5 in an array. There may be a way to understand it (...delete [] would know it)
       by inspecting the memory directly for the "header" that the allocator places before the
       array. But it is implementation dependant. And who said that a generic pointer is actually
       pointing to the first element? */
    int* arrayInHeap = new int[5];
    while(true);
}

int main(void)
{
    function();
    return 0;
}