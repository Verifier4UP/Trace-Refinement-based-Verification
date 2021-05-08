// run in sequence: 
// 2-1-2-3-1-2

type A;
function f(x: A) returns (A);
function u(x: A) returns (A);


procedure main()
{
    var x, y, z, w, s, r1, r2, r3: A;

    x := y;
    assume(s == r2);
    while (y != z){
        if (s == r1) {
            x := f(x);
            s := u(s);
            assume(s != r1);
            assume(s != r2);
            assume(s != r3);
        } else {
            if (s == r2) {
                x := f(x);
                y := f(y);
                s := u(s);
                if (y == w){
                    assume(s == r1);
                } else {
                    assume(s == r3);
                }
            } else {
                if (s == r3) {
                    y := f(y);  
                    x := f(x);
                    s := u(s);
                    if (y == w){
                        assume(s == r1);
                    } else {
                        assume(s == r2);
                    }
                } else {
                    y := f(y);
                    s := u(s);
                    assume(s == r2);
                }
            }
        }
    }

    assert(x != y);
}