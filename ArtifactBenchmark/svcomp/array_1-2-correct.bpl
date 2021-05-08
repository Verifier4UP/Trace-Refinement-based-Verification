// check after assignment

type A;
function f(x: A) returns (A);
function next(x: A) returns (A);


procedure main()
{
    var x, y, star, ret_x, ret_y: A;

    assume(x != star);
    while (x != star){
        ret_x := f(x);
        assume(x == ret_x);
        y := x;
        x := next(x);
    }
    ret_y := f(y);

    assert(y == ret_y);
}