/* Test what happens if there are local variables of primitive types in a stack trace.
   Some may have to be represented, but none of them should be visited. */
int main(void)
{
    int does_not_count;  // Not a pointer, we don't care.
    int* null_pointer = nullptr;
    int* optimized_out_1 = &does_not_count;
    int& optimized_out_2 = does_not_count;

	while(true);
	return 0;
}
