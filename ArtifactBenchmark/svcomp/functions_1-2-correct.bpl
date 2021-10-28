// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y, star, ret_x, ret_y: A;

    y := f(x);
    while (x != star){
        x := f(x);
        y := f(y);
    }
    ret_x := f(x);

    assert(y == ret_x);
}