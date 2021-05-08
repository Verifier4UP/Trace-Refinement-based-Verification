// check after assignment

type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, z, r, t: A;

    y := z;
    while (x != z){
        x := f(x);
    }
    while (r != t){
        x := f(x);
        y := f(y);
        r := f(r);
    }

    assert(x == y);
}