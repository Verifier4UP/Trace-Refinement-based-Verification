// check after assignment

type A;
function f(x: A) returns (A);

procedure main()
{
    var x, y, z, w: A;

    x := y;
    while (y != z){
    	if (y != w){
    		y := f(y);
    	} else {
    		z := f(z);
    	}
    }

    assert(x == y);
}