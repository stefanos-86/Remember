struct Level3 {
	char placeholder;
};

struct Level2 {
	Level3 *  p = new Level3();
};

struct Level1 {
	Level2 *  p = new Level2();
};


void anotherFunction() {
	Level2 * inFunction = new Level2();
	int * pointerToInt = nullptr;
	while(true);  // Hold it here to dump a core.
}

void function() {
	char * pointToChar;
	anotherFunction();
}

int main(void)
{
	Level1 * insideMain = new Level1();
	Level3 * insideMain2 = new Level3();
	function();
	
	return 0;
}