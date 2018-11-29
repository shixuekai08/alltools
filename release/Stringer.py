__author__ = 'shixuekai'

import re

#去掉多余的\n
def DisposeOfLineBreak(string):
    s = re.sub("\n(\n)+", "\n", string)
    if s.endswith("\n"):
        s = s[0: len(s)-1]

    if s.startswith("\n"):
        s = s[1: len(s)]

    return s


#增加顺序标记
def AddSequence(string):
    count = 2
    s = "1 "
    for x in string:
        if x == "\n":
            s += "\n"+str(count)+" "
            count = count + 1
        else:
            s += x

    return s