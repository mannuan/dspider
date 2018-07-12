#使用pickle模块将数据对象保存到文件

import pickle

da = {'a': [1, 2.0, 3, 4+6j],
         'b': ('string', u'Unicode string'),
         'c': None}

selfref_list = [1, 2, 3]
selfref_list.append(selfref_list)

output = open('/home/wjl/data.pkl', 'wb')

# Pickle dictionary using protocol 0.
pickle.dump(da, output)

# Pickle the list using the highest protocol available.
pickle.dump(selfref_list, output, -1)

output.close()

#使用pickle模块从文件中重构python对象

import pprint, pickle

pkl_file = open('/home/wjl/data.pkl', 'rb')

data1 = pickle.load(pkl_file)
pprint.pprint(data1)

data2 = pickle.load(pkl_file)
pprint.pprint(data2)

pkl_file.close()