/* Test what happens if there are local variables of primitive types in a stack trace.
   Some may have to be represented, but none of them should be visited. */
int main(void)
{
    int does_not_count;  // Not a pointer, we don't care.
    int* null_pointer = nullptr;
    int* unresolvable = &does_not_count;  // Can't figure out how big the main frame is, so can't find this pointer.

	while(true);
	return 0;
}
