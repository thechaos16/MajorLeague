# -*- coding: utf-8 -*-
# set of functions for any modules

def isNumber(string):
    try:
        float(string)
        return True
    except ValueError:
        return False
