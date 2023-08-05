# CJK Format

This Python 3 module provides utility functions for formatting fixed-width CJK strings. One of the most important features of tihs module is to align Latin and CJK characters using `%{width}s` specifiers. For example, the following lines
```python
print('%-10s|%-10s|' % ('ab', 'cd'))
print('%-10s|%-10s|' % ('가나다라', '마바사아'))
```
will print misaligned lines between Latin and CJK characters even with the `%-10s` specifiers.

Now, using this module's `f()` function, the above example would be
```python
from cjkformat import f

print(f('%-10s|%-10s|', 'ab', 'cd'))
print(f('%-10s|%-10s|', '가나다라', '마바사아'))
```
which will print nicely aligned output.

The module also defines a shortcut function `printf()` to minic the same function in the C language. For example,
```python
from cjkformat import printf

printf('%-10s|%-10s|\n', 'ab', 'cd')
printf('%-10s|%-10s|\n', '가나다라', '마바사아')
```

For more information, please visit [the GitHub repository](https://github.com/HuidaeCho/cjkformat).
