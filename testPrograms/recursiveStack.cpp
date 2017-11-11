void  recursion(int level) {
	int * pointer;

	if (level == 0)
		while(true);

	recursion(level -1);
}

int main(void)
{
	recursion(10);
	return 0;
}
