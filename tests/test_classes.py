class Clazz:
    clazz_attribute = "class attr."

    def __init__(self):
        self.instance_attribute = "inst. attr."

    def instance_method(self):
        """
        allows to modify the instance and class state by accessing instance
        and class attributes
        :return:
        """
        assert self.__class__.clazz_attribute == "class attr."
        return "inst. method"

    @classmethod
    def class_method(cls):
        """
        allows to modify the class state only by accessing to class attributes;
        the changes are propagated to all class instances
        :return:
        """
        assert cls is Clazz
        return "class method"

    @staticmethod
    def static_method():
        """
        allows access neither to instance nor class attributes; used to namespace methods
        :return:
        """
        return "static method"


def test_instance_method():
    c = Clazz()
    assert c.instance_attribute == "inst. attr."
    assert c.__class__.clazz_attribute == "class attr."
    assert c.instance_method() == "inst. method"
    assert Clazz.instance_method(c) == "inst. method"


def test_class_method():
    assert Clazz.class_method() == "class method"
    assert Clazz.clazz_attribute == "class attr."


def test_static_method():
    assert Clazz.static_method() == "static method"
