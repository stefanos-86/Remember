/* Cycle of pointers in the heap. Must not have infinite loops! */

struct Object
{
    Object* p;
};

int main(void)
{
    Object* go_forward = new Object();
    Object* go_backward = new Object();

    go_backward->p = go_forward;
    go_forward->p = go_backward;

    while(true);
}