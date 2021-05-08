// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y, s, t, star: A;

    x := y;
    assume(x != star);
    assume(s == t);
    while (x == star){
        if (s == t){
            x := f(x);
            y := f(y);
        } else {
            x := f(x);
        }
    }

    assert(x != y);
}