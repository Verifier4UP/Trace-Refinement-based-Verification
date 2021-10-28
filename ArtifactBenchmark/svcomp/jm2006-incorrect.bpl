// check after assignment

type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, star, s, t: A;

    x := t;
    y := s;
    assume(x != star);
    while (x != star){
        x := f(x);
        y := f(y);
    }
    assume(t == s);

    assert(y != star);
}