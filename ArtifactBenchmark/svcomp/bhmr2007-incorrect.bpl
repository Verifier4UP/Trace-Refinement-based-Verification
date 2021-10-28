// check after assignment

type A;
function f(x: A) returns (A);
function h(x: A) returns (A);

procedure main()
{
    var x, y, star, s, t: A;

    assume(x != star);
    while (x != star){
    	if (s == t){
    		x := f(x);
    		y := h(y);
    		assume(x == y);
    		s := f(s);
    	} else {
    		x := h(x);
    		y := f(y);
    		assume(x == y);
    		t := f(t);
    	}
    }

    assert(x != y);
}