// check after assignment

type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, star1, star2: A;

    assume(x != star1);
    while (x != star1){
    	y := x;
    	while (y != star2){
    		y := f(y);
    	}
    	x := f(x);
    }

    assert(y != star2);
}