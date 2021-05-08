type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, z: A;
    x := y;
    while (x != z) {
        x := f(x);
        y := f(y);
    }
    assert(x == y);
}