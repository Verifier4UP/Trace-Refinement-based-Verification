type A;
function f(x: A) returns (A);
function h(x: A) returns (A);

procedure main()
{
  var x, y, z, t, s, k: A;
  x := t;
  y := k;
  if (t != s){
    assume(t == k);
    while (y != z)
    {
      x := f(x);
      y := f(y);
      z := h(z);
    }
  }else{
    while (y != z)
    {
      x := f(x);
      y := f(y);
      z := h(z);
    }
    assume(t == k);
  }
  assert(x == y);
}