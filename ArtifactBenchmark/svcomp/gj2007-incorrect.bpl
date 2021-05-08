// check after assignment

type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, star, ret_x: A;

    y := f(x);
    while (y != star){
        x := f(x);
        y := f(y);
    }
    ret_x := f(x);

    assert(ret_x != star);
}