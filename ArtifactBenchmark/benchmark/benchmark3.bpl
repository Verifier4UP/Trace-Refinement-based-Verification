type A;
function f(x: A) returns (A);
function h(x: A) returns (A);
procedure main(){

	var k, r0, s, t, u3, u5, v4, v6, x, y, z: A;

	x := y;

	if (s == u5) {
		x := t;
		y := k;
		while (y != z){
			x := f(x);
			y := f(y);
			z := f(z);
		}
		assume(t == k);
	} else {
			if (s == u3) {
				x := f(x);
				y := f(y);
				x := h(x);
				y := h(y);
			}
	}

	if (s == r0) {
		x := f(x);
		y := f(y);
	} else {
			if (s == v4) {
				x := f(x);
				x := h(x);
				y := f(y);
				y := h(y);
			}
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
		y := f(y);
	}

	assert(x == y);
}