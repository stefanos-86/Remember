/*Check that we can follow the pointers indide objects. */
struct Level3 {
	char placeholder;
};

struct Level2 {
	Level3 *  p = new Level3();
};

struct Level1 {
	Level2 *  p = new Level2();
};


int main(void)
{
    Level1* head = new Level1();
    while(true);
}