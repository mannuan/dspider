# -*- coding:utf-8 -*-

import re

print(re.sub(r'^[^\(]*\(([\d]+)[^\)\d]*\)$',r'\1','4.3分(2586人点评)'))

