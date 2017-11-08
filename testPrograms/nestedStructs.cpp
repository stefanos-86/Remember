struct Level3
{
	char y;
};

struct Level2
{
	Level3 *  p = new Level3();
};

struct Level1
{
	Level2 *  p = new Level2();
};

int main(void)
{
	Level1 * insideMain = new Level1();
	
	while(true);
	
	return 0;
}