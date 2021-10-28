// check after assignment

type A;
function f(x: A) returns (A);
function next(x: A) returns (A);

procedure main()
{
    var x, y, star, ret_x, ret_y, t: A;

    assume(x != star);
    while (x != star){
        y := x;
        ret_x := f(x);
        assume(ret_x == t);
        x := next(x);
    }
    ret_y := f(y);

    assert(ret_y == t);
}