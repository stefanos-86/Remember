

void  recursion(int level) {
	int * pointer;

	if (level == 0)
		while(true);

	recursion(level -1);
}

int main(void)
{
	int x;
	int *y = 0;
	int *z = &x;

	recursion(10);
	return 0;
}
