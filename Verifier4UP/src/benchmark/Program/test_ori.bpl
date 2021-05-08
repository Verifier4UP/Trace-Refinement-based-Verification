type A;
function f(x: A) returns (A);
function h(x: A) returns (A);

procedure main()
{
    var x, y, z, t, s, k: A;
    x := t;
    y := k;
    assume(t == s);
    while (y != z)
    {
      x := f(x);
      y := f(y);
      z := h(z);
    }
    assume(t == k);
    assert(x == y);
}