# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.

"""

def function_example(foo, bar, baz=None):
    """Creates an example docstring.
    
    Args:
        foo (int): First parameter and type.
        bar (str): Second paramater and type.
        baz (int): Third parameter defaults to None.
        
    Returns:
        bool: The return value. True for success, False otherwise
        
    """
    
    if foo == 1:
        return True
    if baz is None:
        baz = []
    return False