// check after assignment

type A;
function f(x: A) returns (A);


procedure main()
{
    var x, star: A;

    assume(x != star);
    while (x != star){
        x := f(x);
    }

    assert(x == star);
}