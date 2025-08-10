"""
Helper function for evaluating formula expression

Includes:
- get_request()
"""

from simpleeval import SimpleEval

def formula_eval(val, formula):
    """
    To evaluate a string formula expression and return results
    :param val: dict, List will formula variable as keys and its values
    :param formula: string format formula expression
    :return: float, result of the formula
    """

    s = SimpleEval()
    s.names = val

    return round(s.eval(formula), 2)