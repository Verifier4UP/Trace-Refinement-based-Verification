// check after assignment

type A;
function f(x: A) returns (A);
function increase(x: A) returns (A);
function decrease(x: A) returns (A);


procedure main()
{
    var x, y, w0, w1, z0, z1: A;

    w0 := w1;
    z0 := z1;
    x := y;

    while (w0 != z0){
        x := decrease(x);
        w0 := f(w0);
    }
    while (w1 != z1){
        x := increase(x);
        w1 := f(w1);
    }

    assert(x == y);
}