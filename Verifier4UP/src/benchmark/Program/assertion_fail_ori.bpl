type A;
function f(x: A) returns (A);
function g(x: A) returns (A);

procedure main()
{
  var x, y, z, t, s: A;
  x := t;
  y := t;
  if (t != s){
    x := s;
    y := s;
  }else{
    while (y != z)
    {
      x := f(x);
      y := g(y);
      z := g(z);
    }
  }
  assert(x == y);
}