
def is_alnum_underscore(name):
    """ Check str contain only alphanumeric characters and underscore ('_')

    Args:
        name (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    return re.match("^[a-zA-Z0-9_]+$", name) is not None


def is_alnum_underscore_dash_dot(name):
    """ Check str just contains alphabets, numbers, dash, dot and underline

    Args:
        name (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    return re.match("^[a-zA-Z0-9._-]+$", name) is not None


def is_alnum_underscore_dash_dot_ampersand_parentheses(name):
    """ Check str just contains alphabets, numbers, dash, dot, ampersand, parentheses and  underline

    Args:
        name (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    return re.match("^[a-zA-Z0-9&()._-]+$", name) is not None


def check_valid_name(name):
    if len(name) > 15:
        raise ErrorInvalidName("length of %s is not valid" % name)

    if name.startswith("-") or name.startswith("_"):
        raise ErrorInvalidName(name)

    if re.match("^[A-Za-z0-9_-]*$", name) is None:
        raise ErrorInvalidName(name)
    return True


def is_alnum_underscore_dash(name):
    """ Check str just contains alphabets, numbers, dash and underline

    Args:
        name (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    return re.match("^[a-zA-Z0-9_-]+$", name) is not None


def is_alphanumeric_underscore(name):
    """ Check str just contains alphabets, numbers and underline

    Args:
        name (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    return re.match("^[a-zA-Z0-9_]+$", name) is not None


def is_digit(name):
    """ Checks name be an integer number.

    Args:
        name (str): Name to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        if name.isdigit():
            return True

    except:
        logger.exception("is_digit: '%s'", name)
    return False

  def is_float(value):
    """ Checks value to be a float number

    Args:
        value (str): String to be checked.

    Returns:
        bool: True if successful, False otherwise.
    """
    try:
        float(value)
        return True
    except ValueError:
        logger.exception("is_float: '%s'", value)
        return False
