type A;
function f(x: A) returns (A);
function g(x: A) returns (A);


procedure main()
{
    var x, y, w, z: A;
    x := y;
    while (x != z) {
        x := f(x);
        y := f(y);
    }
    while (x != w) {
        x := g(x);
        y := g(y);
    }
    assert(x == y);
}
