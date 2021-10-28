type A;
function f(x: A) returns (A);
function h(x: A) returns (A);
procedure main(){

	var k, r0, s, t, u5, v2, v6, x, y, z: A;

	x := y;

	if (s == r0) {
		x := f(x);
		y := f(y);
	} else {
		x := f(x);
		y := f(y);
	}

	if (s == v6) {
		x := t;
		y := k;
		assume(t == k);
		while (y != z){
			x := f(x);
			y := f(y);
			z := f(z);
		}
	} else {
		x := f(x);
	}

	if (s == v2) {
		x := f(t);
		y := f(k);
		x := h(x);
		y := h(y);
		assume(t == k);
	} else {
			if (s == u5) {
				x := t;
				y := k;
				while (y != z){
					x := f(x);
					y := f(y);
					z := f(z);
				}
				assume(t == k);
			}
	}

	assert(x == y);
}