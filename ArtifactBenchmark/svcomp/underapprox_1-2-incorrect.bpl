// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y, tmp, ret, star: A;

    tmp := x;
    x := f(x);
    y := tmp;
    while (x != star){
        x := f(x);
        y := f(y);
    }
    ret := f(y);

    assert(ret != x);
}