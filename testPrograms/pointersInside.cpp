/*Test that we can chase pointers "hidden" inside stack objects or class members.*/

struct HasPointer
{
    char* x = nullptr;
};

struct PointersInMemebers
{
    HasPointer insideThisOne;
};

void function()
{
    HasPointer inFunction;
    PointersInMemebers deepInside;

    while(true);
}

int main(void)
{
    function();
    return 0;
}