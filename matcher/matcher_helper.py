import copy
import hashlib
import sys
import time
import random

import subprocess32

from error_classes import SysCommandError, SysCommandTimeout

def call_stub(cmd, by_shell=False, ignore_return_code=False, cwd=None, timeout=180, no_log=False):
    """ Executes a shell command

    Args:
        cmd (str): Shell command
        by_shell (bool): True if command should be executed using shell
        ignore_return_code (bool): True if no exception should be raised in case of non-zero error code
        cwd (str): Working directory to run command
        timeout(int or None): time in second to wait for command to return return_code
        no_log(bool): disable auto logging

    Returns:
        helper.StubOutput: An object of helper.StubOutput
    """
    import sab
    return_code = -1
    cout = cerr = ""
    try:
        if not by_shell:

            array_command = cmd.split()
            proc = subprocess32.Popen(array_command, stdout=subprocess32.PIPE,
                                      stderr=subprocess32.PIPE, cwd=cwd)
        else:

            proc = subprocess32.Popen(cmd, shell=True, stdout=subprocess32.PIPE,
                                      stderr=subprocess32.PIPE, executable='/bin/bash', cwd=cwd)
        cout, cerr = proc.communicate(timeout=timeout)
        return_code = proc.returncode

        if sab.SERVICE_TERM:
            sys.exit(1)

        if ignore_return_code is False and return_code is not 0:
            raise SysCommandError(return_code, cout, cerr, cmd)
    except subprocess32.TimeoutExpired:
        raise SysCommandTimeout(cmd, timeout)
    except BaseException as e:
        if not isinstance(e, SystemExit):
            raise SysCommandError(return_code, cout, cerr, cmd)
        else:
            raise e
    return cout, cerr, return_code


def convert_text_to_separated_parts(input_text, find_string, add_string):
    """This function reads a text and if found a line is started with find_string string, add new line below it.

    Args:
        input_text (str): String to be read.
        find_string (str): String to be find.
        add_string (str): String to be add.

    Returns:
        str: Modified text.
    """
    output = ""
    for line in input_text.splitlines():
        output += line + "\n"
        if line.strip().startswith(find_string):
            output += add_string + "\n"
    return output


def compare_arrays(new_array, old_array, search_key="name"):
    """Compare two arrays and returns list of the same items, added_item and removed_items lists

    Args:
        new_array (list): New array
        old_array (list): Old array
        search_key (str): Key to be searched in arrays

    Returns:
        tuple: (same_items_list, added_items_list, removed_item_list)
    """

    added_items = copy.copy(new_array)
    removed_items = copy.copy(old_array)
    same_items = []
    for item in new_array:
        if isinstance(item, dict):
            name = item[search_key]
        else:
            name = str(item)
        for obj in old_array:
            if isinstance(obj, dict):
                old_name = obj[search_key]
            else:
                old_name = str(obj)
            if old_name == name:
                same_items.append(obj)
                removed_items.remove(obj)
                added_items.remove(item)

    return same_items, added_items, removed_items


def file_lines_remover(path, line_matcher, remove_empty=True):
    """ Removes special lines if matcher returns true.

    Args:
        path (str):
        line_matcher(function):
        remove_empty (bool): remove empty lines

    Returns:
        None
    """
    new_lines = []
    with open(path, 'r') as reader:
        for line in reader.readlines():
            if line_matcher(line) or (remove_empty and len(line.strip()) == 0):
                continue
            new_lines.append(line)

    with open(path, 'w') as writer:
        for line in new_lines:
            writer.write(line)
            
            
def generate_random_string(length, allowed_chars, key="A SECRET KEY"):
    """ Generates random string of specific length and by secret key

    Args:
        length (int): length of the generated string
        allowed_chars (list of str): allowed characters in the string
        key (str): secret key

    Returns:
        str
    """
    hash_fmt = "%s%s%s" % (random.getstate(), time.time(), key)

    random.seed(hashlib.sha256(hash_fmt.encode('utf-8')).digest())

    return ''.join(random.choice(allowed_chars) for i in range(length))
