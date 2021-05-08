// check after assignment

type A;
function f(x: A) returns (A);
function u(x: A) returns (A);

procedure main()
{
    var x, y, z, s, t: A;

    x := y;
    assume(s != t);
    while (s != t){
        z := f(z);
    }

    assert(x == y);
}