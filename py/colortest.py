"""
creation: unknown

ANSI escape code test. Try it out with `python3 colortest.py`
"""

colors = ['\033[{}m'.format(str(color)) for color in range(108)]

for num, color in enumerate(colors):
    print('{}[{}]aaaaaa\033[m'.format(color, num))