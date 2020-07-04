from string import Template

EXPECTED = "Hey Bob, there is a 0xbadc0ffee error!"


# -- Python 2 old style (printf-like)


def test_old_style_formatting_with_single_arg():
    name = "Bob"
    assert "Hello, %s!" % name == "Hello, Bob!"


def test_old_style_formatting_with_multiple_args():
    name, errno = "Bob", 50159747054
    # %-operator only takes one argument, therefore the right-hand side must be wrapped in a tuple
    actual = "Hey %s, there is a 0x%x error!" % (name, errno)
    assert actual == EXPECTED


def test_old_style_formatting_with_args_referred_by_name():
    name, errno = "Bob", 50159747054
    # argument order doesn't matter
    actual = "Hey %(name)s, there is a 0x%(errno)x error!" % {
        "name": name,
        "errno": errno,
    }
    assert actual == EXPECTED


# -- Python 3 new style, back-ported to Python 2


def test_new_style_formatting_with_single_arg():
    name = "Bob"
    assert "Hello, {}!".format(name) == "Hello, Bob!"


def test_new_style_formatting_with_multiple_args():
    name, errno = "Bob", 50159747054
    actual = "Hey {}, there is a 0x{:x} error!".format(name, errno)
    assert actual == EXPECTED


def test_new_style_formatting_with_args_referred_by_name():
    name, errno = "Bob", 50159747054
    actual = "Hey {name}, there is a 0x{errno:x} error!".format(name=name, errno=errno)
    assert actual == EXPECTED


# -- Python 3.6+ Formatted String Literals


def test_f_string_with_single_expression():
    name = "Bob"
    assert f"Hello, {name}!" == "Hello, Bob!"


def test_f_string_with_inline_arithmetic():
    a, b = 5, 10
    actual = f"Five plus ten is {a + b} and not {2 * (a + b)}."
    assert actual == "Five plus ten is 15 and not 30."


def test_f_string_with_multiple_expressions():
    name, errno = "Bob", 50159747054
    actual = f"Hey {name}, there is a {errno:#x} error!"
    assert actual == "Hey Bob, there is a 0xbadc0ffee error!"


# -- Template Strings


def test_string_template_with_single_arg():
    name = "Bob"
    t = Template("Hey, $name!")
    assert t.substitute(name=name) == "Hey, Bob!"


def test_string_template_with_multiple_arg():
    name, errno = "Bob", 50159747054
    t = Template("Hey $name, there is a $error error!")
    # template strings don’t allow format specifiers, values other than string must be converted to string
    actual = t.substitute(name=name, error=hex(errno))
    assert actual == "Hey Bob, there is a 0xbadc0ffee error!"
