# expand_string

This library provides functions that allow you to expand a string
that contains parenthesis with numeric-values, and then expands that
into an actual string value.


# Installation

````bash
$ pip install expand_string
````

# Usage

Simple example:

````python
from expand_string import expand_string

expand_string('N3(S)N2(E3(NW))')
````

Would result in the output:

```bash
NSSSNENWNWNWENWNWNW
```
Shell example:
```bash
python -m expand_string 'N3(S)N2(E3(NW))'
```

Would result in the output:

```bash
NSSSNENWNWNWENWNWNW
```

For more details see the `expand_string` docstring.
