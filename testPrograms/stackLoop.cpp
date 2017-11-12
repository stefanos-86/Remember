/* Strange case of pointer that goes into a "later" stack frame.
Creates a loop of pointers in the stack. */

#include <stdio.h>
void function_high(int ** x) {  // X points to the lower function.
	int y;                      // Y is pointed at by the lower function.
	(*x) = &y;

    printf("%p\n", &y);  // Prevent optimization of the last assignement.
    while(true);
}

void function_low()
{
    int * willBeSetToPointAtFunctionVariable;
    function_high(&willBeSetToPointAtFunctionVariable);
}

int main(void)
{
    function_low();
	return 0;
}