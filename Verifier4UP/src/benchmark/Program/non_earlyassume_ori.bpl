type A;
function f(x: A) returns (A);

procedure main()
{
  var x, y, r, s, t: A;
  x := t;
  y := t;
  if (t != s){
    x := s;
    y := s;
  }else{
    x := f(t);
    y := f(r);
    x := f(x);
    y := f(y);
    assume(t == r);
  }
  assert(x == y);
}