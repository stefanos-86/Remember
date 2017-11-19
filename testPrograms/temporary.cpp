/* What happens with temporary parameters?
   They are seen as parameters of the receiving function. */


class SomeKindOfClass{};

void upperFunction(const SomeKindOfClass& temporary)
{
    while(true);
}

void function()
{
    upperFunction(SomeKindOfClass());
}

int main()
{
    function();
    return 0;
}