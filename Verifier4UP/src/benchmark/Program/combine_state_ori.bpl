type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, z0, z1, w0, w1: A;
    z0 := z1;
    z0 := f(z0);
    z1 := f(z1);
    x := z0;
    y := z1;
    z0 := f(z0);
    z1 := f(z1);
    w0 := z0;
    w1 := z1;
    assert(x == y);
}