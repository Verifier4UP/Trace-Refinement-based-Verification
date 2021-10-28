// check after assignment

type A;
function f(x: A) returns (A);
function m(x: A) returns (A);
function h(x: A) returns (A);
function add(x: A, y: A) returns (A);
function next(x: A) returns (A);


procedure main()
{
    var x, y, z, w, u, i, j, k, ret_add, ret_xy: A;

    x := i;
    y := j;
    z := k;
    ret_add := add(i, j);
    assume(k == ret_add);

    while (z != w){
        i := f(i);
        j := m(j);
        k := h(k);
        ret_add := add(i, j);
        assume(k == ret_add);
        if (z != u){
            x := i;
            y := j;
            z := k;
        }
        w := next(w);
    }
    ret_xy := add(x, y);
    
    assert(z != ret_xy);
}