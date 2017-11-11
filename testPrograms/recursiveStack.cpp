void  recursion(int level) {
	int * pointer;  // Will be optimized out, even at -O0

	if (level == 0)
		while(true);

	recursion(level -1);
}

int main(void)
{
	recursion(10);
	return 0;
}
