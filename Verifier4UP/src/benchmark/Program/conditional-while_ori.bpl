type A;
function f(x: A) returns (A);
function h(x: A) returns (A);
function k(x: A) returns (A);

procedure main()
{
  var x, y, s, t, r1, r2: A;
  x := y;
  while (s != t){
    if (r1 == r2){
        x := f(x);
        y := f(y);
        r1 := k(r1);
        assume(r1 != r2);
    } else {
        x := h(x);
        y := h(y);
        r2 := k(r2);
        assume(r1 == r2);
    }
    t := k(t);
  }
  assert(x == y);
}