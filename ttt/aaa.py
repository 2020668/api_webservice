# -*- coding: utf-8 -*-
"""

=================================
Author: keen
Created on: 2019/6/24

E-mail:keen2020@outlook.com

=================================


"""

import re

str = 'pythonhsgjgthashgpython'
res = re.findall(r'py(th)on', str)
print(res)

