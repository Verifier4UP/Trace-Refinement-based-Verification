// check the correctness of traverse

type A;
function f(x: A) returns (A);
function next(x: A) returns (A);


procedure main()
{
    var x, y, t, star, ret_x, ret_y: A;

    assume(x != star);
    while (x != star){
        ret_x := f(x);
        assume(ret_x == t);
        y := x;
        x := next(x);
    }
    ret_y := f(y);

    assert(ret_y == t);
}