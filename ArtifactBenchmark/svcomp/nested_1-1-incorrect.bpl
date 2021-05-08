// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y, star, ret_x, ret_y: A;

    assume(x != star);
    while (x != star){
        y := x;
        while (y != star){
        	y := f(x);
        }
        x := f(x);
    }

    assert(y != star);
}