from app.calculations import add 


def test_add():
    print("testing add function")
    sum = add(1, 2)
    assert sum == 3


