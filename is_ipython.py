# This function checks if the program is running in IPython, since IPython does not support printing subprocess messages synchronously
def is_ipython():
    try:
        get_ipython().__class__.__name__
        return True
    except NameError:
        return False