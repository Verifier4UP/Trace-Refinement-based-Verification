// check after assignment

type A;
function f(x: A) returns (A);
function h(x: A) returns (A);

procedure main()
{
    var x, y, star, ret: A;

    assume(x != star);
    while (x != star){
        y := x;
        if (x != star){
            x := f(x);
        } else{
            x := h(x);
        }
    }
    ret := f(y);

    assert(x != ret);
}