// check after assignment

type A;
function f(x: A) returns (A);
function h(x: A) returns (A);
function add(x: A, y: A) returns (A);

procedure main()
{
    var x, y, star, add_xy, t, ret: A;

	assume(x != star);
    while (x != star){
        x := f(x);
        y := h(y);
        add_xy := add(x, y);
        assume(add_xy == t);
    }
    ret := add(star, y);

    assert(ret != t);
}