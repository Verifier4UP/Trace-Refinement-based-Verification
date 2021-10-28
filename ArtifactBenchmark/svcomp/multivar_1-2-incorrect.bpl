// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y, star: A;

    x := y;
    while (x != star){
        x := f(x);
        y := f(y);
    }

    assert(x != y);
}