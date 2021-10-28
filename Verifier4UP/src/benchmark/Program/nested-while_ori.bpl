type A;
function f(x: A) returns (A);
function h(x: A) returns (A);

procedure main()
{
  var x, y, z, s, t: A;
  x := z;
  y := z;
  while (s != t){
    x := f(x);
    z := f(z);
    s := h(s);
    while (y != z){
        y := h(y);
    }
  }
  assert(x == y);
}