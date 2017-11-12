/* Test that we can handle references just as we would pointers. */

struct IsReferenced {};

struct HasReference
{
    HasReference(IsReferenced& r) : reference(r) {}
    IsReferenced& reference;
};


void function(void)
{
    IsReferenced* x = new IsReferenced();
    HasReference* y = new HasReference(*x);
    while(true);
}


int main(void)
{
    function();  // Known limit: can't find objects in the main frame.
}