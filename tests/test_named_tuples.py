from collections import namedtuple

from recordtype import recordtype


def test_create_namedtuple_from_string(capsys):
    # using namedtuple is a way shorter than defining a class manually
    Car = namedtuple("Car", "color mileage")
    car = Car("red", 3812.4)
    # "Car" class works as expected
    assert car.color == "red"
    assert car.mileage == 3812.4
    # each namedtuple is represented by its own class, which is created
    # by using the namedtuple() factory function
    print(car)
    captured = capsys.readouterr()
    assert captured.out == "Car(color='red', mileage=3812.4)\n"
    # like tuples, named tuples are immutable
    # car.color ='blue'  # => AttributeError: can't set attribute


def test_create_namedtuple_from_list():
    Car = namedtuple("Car", ["color", "mileage"])
    car = Car("red", 3812.4)
    assert car.color == "red"
    assert car.mileage == 3812.4


def test_get_all_field_values_as_list():
    Car = namedtuple("Car", "color mileage")
    car = Car("red", 3812.4)
    assert list(car) == ["red", 3812.4]


def test_change_named_tuple_value():
    Car = namedtuple("Car", "color mileage")
    car = Car("red", 3812.4)
    car2 = car._replace(color="blue")
    assert list(car) == ["red", 3812.4]
    assert list(car2) == ["blue", 3812.4]


def test_create_record_type_from_string():
    Car = recordtype("Car", "color mileage")
    car = Car("red", 3812.4)
    assert list(car) == ["red", 3812.4]


def test_create_record_type_from_list():
    Car = recordtype("Car", ["color", "mileage"])
    car = Car(color="red", mileage=3812.4)
    assert list(car) == ["red", 3812.4]


def test_change_record_type_value():
    Car = recordtype("Car", "color mileage")
    car = Car("red", 3812.4)
    car.color = "blue"
    assert list(car) == ["blue", 3812.4]
