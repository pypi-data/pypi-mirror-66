from .exceptions import StringExpressionError


def expand_string(str_expression):
    """
    Helper function to expand string expression. Examples;
        N3(S)N2(E3(NW)) => NSSSNENWNWNWENWNWNW
    :param str_expression: a string containing parenthesis to be expanded
    :return: expanded string (string without parenthesis)
    """

    multiples = [1]
    full_string = []
    buffered_int = None
    open_parenthesis_count = 0

    for char in str_expression:
        try:
            mul = int(char)
            if buffered_int:
                multiples and multiples.pop()
                mul = int('%s%s'%(buffered_int, mul))
            multiples.append(multiples[-1]*mul)
            buffered_int = mul
        except ValueError:
            buffered_int = None
            if char == '(':
                open_parenthesis_count += 1
            elif char == ')':
                multiples and multiples.pop()
                open_parenthesis_count -= 1
            else:
                full_string.append(multiples[-1]*char)

    if open_parenthesis_count:
        raise StringExpressionError('Mismatching opening and closing parenthesis')

    return ''.join(full_string)
