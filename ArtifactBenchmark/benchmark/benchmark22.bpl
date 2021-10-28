type A;
function f(x: A) returns (A);
function h(x: A) returns (A);
function l(x: A) returns (A);
procedure main(){

	var k, s, t, u1, u7, v6, w1, w2, w3, w4, x, y, z: A;

	x := y;

	if (s == u1) {
		x := f(t);
		y := f(k);
		assume(t == k);
		x := h(x);
		y := h(y);
	} else {
		x := f(x);
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

	if (s == u7) {
		while (w1 != w2) {
			if (w3 == w4) {
				x := f(x);
				y := f(y);
				w3 := l(w3);
				assume(w3 != w4);
			} else {
				x := h(x);
				y := h(y);
				w4 := l(w4);
				assume(w3 == w4);
			}
			w1 := f(w1);
		}
	} else {
		x := f(x);
	}

	assert(x == y);
}