// check after assignment


type A;
function f(x: A) returns (A);


procedure main()
{
    var x, y: A;

    assume(x != y);
    while (x != y){
        x := f(x);
    }

    assert(x == y);
}