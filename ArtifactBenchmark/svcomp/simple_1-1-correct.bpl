// check after assignment

type A;
function f(x: A) returns (A);
function even(x: A) returns (A);


procedure main()
{
    var x, star, ret, T: A;

    assume(x != star);
    while (x != star){
        x := f(x);
        ret := even(x);
        assume(ret == T);
    }
    ret := even(x);

    assert(ret == T);
}