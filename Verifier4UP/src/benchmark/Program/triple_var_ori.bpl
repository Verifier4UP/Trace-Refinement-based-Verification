type A;
function f(x: A) returns (A);

procedure main()
{
  var x, y, w, z, s, r0, r1, r2: A;
  x := w;
  y := w;
  assume(r0 != r1);
  assume(r0 != r2);
  assume(r1 != r2);
  assume(s != r1);
  while (w != z)
  {
    if (s == r0){
      x := f(x);
      s := r1;
    }
    else {
      if (s == r1){
        y := f(y);
        s := r2;
      }
      else {
        if (s == r2){
          w := f(w);
          s := r0;
        }
      }
    }
  }
  assert(x == y);
}