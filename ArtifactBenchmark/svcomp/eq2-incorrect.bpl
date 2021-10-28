// check after assignment

type A;
function f(x: A) returns (A);
function u(x: A) returns (A);

procedure main()
{
    var x, y, z, w, t, s: A;

    x := w;
    y := f(x);
    z := f(w);
    while (t != s){
        y := u(y);
        z := u(z);
        t := f(t);
    }

    assert(y != z);
}