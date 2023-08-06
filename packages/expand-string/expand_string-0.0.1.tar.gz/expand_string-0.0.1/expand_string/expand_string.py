from .exceptions import StringExpressionError


def parse_multiples(multiples):
    """
    A function to transform a list representing string nesting into the actual string
    Examples:
        [2, 'NWNWNW', 2, 'W', 'EEEE', 'W'] => NWNWNWWEEEEWWEEEEWNWNWNWWEEEEWWEEEEW
        ['N', 'SSS', 'N', 'EE'] => NSSSNEE
    :param multiples: list representing the string nesting
    :return: a string represented by the multiples
    """
    final_str = ''
    last_index = len(multiples) - 1
    while last_index >= 0:
        mul = multiples[last_index]
        try:
            final_str *= mul
        except TypeError:
            # use this syntax as opposed to '+=' to avoid final_str reversal
            final_str = mul + final_str
        last_index -= 1

    return final_str


def expand_string(str_expression):
    """
    Helper function to expand string expression. Examples;
        2(3(NW)2(W2(EE)W)) => NWNWNWWEEEEWWEEEEWNWNWNWWEEEEWWEEEEW
        N3(S)N2(E3(NW)) => NSSSNENWNWNWENWNWNW
    :param str_expression: a string containing parenthesis to be expanded
    :return: expanded string (string without parenthesis)
    """
    multiples = []
    temp_str = ''
    buffered_int = None
    open_parenthesis_count = 0

    def reset_temp_str(temp_str):
        if temp_str:
            multiples.append(temp_str)
            return ''
        return temp_str

    for char in str_expression:
        try:
            mul = int(char)
            temp_str = reset_temp_str(temp_str)

            if buffered_int:
                multiples and multiples.pop()
                mul = int(str(buffered_int)+str(mul))
            multiples.append(mul)
            buffered_int = mul
        except ValueError:
            if char == '(':
                temp_str = reset_temp_str(temp_str)
                open_parenthesis_count += 1
                buffered_int = None
            elif char == ')':
                mul = multiples and multiples[-1] or 1
                if temp_str:
                    try:
                        new_str = mul * temp_str
                        multiples and multiples.pop()
                        multiples.append(new_str)
                    except TypeError:
                        multiples.append(temp_str)
                    temp_str = ''
                open_parenthesis_count -= 1
                buffered_int = None
            else:
                temp_str += char
                buffered_int = None

    if open_parenthesis_count:
        raise StringExpressionError('Mismatching opening and closing parenthesis')

    return parse_multiples(multiples) + temp_str
