// check the correctness of traverse

type A;
function next(x: A) returns (A);


procedure main()
{
    var x, y, star: A;

    y := x;
    assume(x != star);
    while (x != star){
        y := x;
        x := next(x);
    }

    assert(y != star);
}