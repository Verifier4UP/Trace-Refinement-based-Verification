// check after assignment

type A;
function f(x: A) returns (A);
function u(x: A) returns (A);
function h(x: A, y: A) returns (A);

procedure main()
{
    var x, y, z, w, r, s, t, ret_1, ret_2: A;

    x := w;
    y := z;
    while (t != s){
        if (t != r){
            x := f(x);
            w := f(w);
        } else {
            y := u(y);
            z := u(z);
        }
        t := f(t);
    }
    ret_1 := h(x, y);
    ret_2 := h(w, z);

    assert(ret_1 != ret_2);
}