void anotherFunction(int* y) {
	int * pointerToY = y;
	while(true);  // Hold it here to dump a core.
}

void function(int* x) {
	int * pointToInt = x;
	int y;
	anotherFunction(&y);
}

int main(void)
{
    int x;
	function(&x);

	return 0;
}