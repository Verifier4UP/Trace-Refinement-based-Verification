// check after assignment

type A;
function f(x: A) returns (A);
function next(x: A) returns (A);

procedure main()
{
    var x, y, s, t, t1, t2, star, ret_x, ret_y, ret_t1, ret_t2: A;

    t1 := x;
    t2 := y;
    assume(x != star);
    while (x != star){
        ret_x := f(x);
        ret_y := f(y);
        assume(ret_x == ret_y);
        if (s == t){
            t1 := x;
            t2 := y;
        } else {
            s := f(s);
        }
        x := next(x);
        y := next(y);
    }
    ret_t1 := f(t1);
    ret_t2 := f(t2);

    assert(ret_t1 != ret_t2);
}