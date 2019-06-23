# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/21

E-mail:keen2020@outlook.com

=================================


"""

import re

str1 = "dhggehrpython asdhgpython"
# math = r'\b[a-z]'\
math = r'python'
# res = re.match(math, str1)
# res = re.findall(math, str1)
res = re.search(math, str1).group()
print(res)

