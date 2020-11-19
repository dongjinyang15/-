'''
import pandas as pd
import numpy as npy
import matplotlib.pyplot as plt
# s = pd.Series([1, 3, 6, npy.nan, 44, 1])
# print(s)
# dates = pd.date_range('20160101', periods=6)
# print(dates)
# df = pd.DataFrame(npy.arange(24).reshape(6, 4), index=dates, columns=['A', 'B', 'C', 'D'])
# print(df)

# 数据选择
# print(df['A'])
# print(df.A)
# print(df[0:3])
# print(df['20160101':'20160103'])
# select by label:loc
# print(df.loc['20160102'])
# print(df.loc[:, ['A', 'B']])

# select by position: iloc
# print(df.iloc[1, 3])

# mixed selection: ix
# ix被移除

# print(df[df.A > 8])

# pandas设置值
# df.iloc[2, 2] = 1111
# df.loc['20160101', 'B'] = 2222

# df['E'] = pd.Series([1, 2, 3, 4, 5, 6], index=pd.date_range("20160101", periods=6))
# print(df)


# 处理丢失数据
# df.iloc[0:2, 2:4] = npy.nan
# print(df)
##print(df.dropna(axis=0))# 丢掉某一行
# print(df.fillna(value=12))

# 导入导出数据


# 合并concatenate
df1 = pd.DataFrame(npy.ones((3, 4))*0, columns=['a', 'b', 'c', 'd'], index=[1, 2, 3])
df2 = pd.DataFrame(npy.ones((3, 4))*1, columns=['b', 'c', 'd', 'e'], index=[2, 3, 4])
# df3 = pd.DataFrame(npy.ones((3, 4))*2, columns=['a', 'b', 'c'])

# res = pd.concat([df1, df2, df3], axis=0, ignore_index=True)

# join,['inner','outer']

res = pd.concat([df1, df2])
print(res)
res = pd.concat([df1, df2], join='inner', ignore_index=True)
print(res)

# join_axes
res = pd.concat([df1, df2], axis=1)
print(res)

# append
res = df1.append(df2, ignore_index=True)
print(res)

# pandas合并merge
left = pd.DataFrame({
    'key': ['K0', 'K1', 'K2', 'K3'],
    'A': ['A0', 'A1', 'A2', 'A3'],
    'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({
    'key': ['K0', 'K1', 'K2', 'K3'],
    'C': ['C0', 'C1', 'C2', 'C3'],
    'D': ['D0', 'D1', 'D2', 'D3']})
res = pd.merge(left, right, on='key')
print(res)

left = pd.DataFrame({'key1': ['K0', 'K0', 'K1', 'K2'],
                             'key2': ['K0', 'K1', 'K0', 'K1'],
                             'A': ['A0', 'A1', 'A2', 'A3'],
                             'B': ['B0', 'B1', 'B2', 'B3']})
right = pd.DataFrame({'key1': ['K0', 'K1', 'K1', 'K2'],
                              'key2': ['K0', 'K0', 'K0', 'K0'],
                              'C': ['C0', 'C1', 'C2', 'C3'],
                              'D': ['D0', 'D1', 'D2', 'D3']})
res = pd.merge(left, right, on=['key1', 'key2'], how='left')

print(res)

# indicator
df1 = pd.DataFrame({'col1': [0, 1], 'col_left':['a', 'b']})
df2 = pd.DataFrame({'col1': [1, 2, 2], 'col_right': [2, 2, 2]})
res = pd.merge(df1, df2, on='col1', how='outer', indicator=True)


# plot data
# Series
data = pd.Series(npy.random.randn(1000),index=npy.arange(1000))
data = data.cumsum()
# DataFrame
data = pd.DataFrame(npy.random.randn(1000, 4),
                    columns=list("ABCD"))
data = data.cumsum()
# data.plot()
ax = data.plot.scatter(x='A', y='B', color='Blue', label='Class 1')
data.plot.scatter(x='A', y='C', color='Green', label='Class 2', ax=ax)
plt.show()
'''

import sys
import numpy as np
import pandas as pd

data = pd.read_csv('D:/python/hw1/train.csv', encoding='big5')

data = data.iloc[:, 3:]  # 前3列数据去掉
data[data == 'NR'] = 0
raw_data = data.to_numpy()  # 转化为numpy数组
month_data = {}

for month in range(12):
    sample = np.empty([18, 480])
    for day in range(20):
        sample[:, 24 * day: 24 * (day + 1)] = raw_data[18 * (20 * month + day): 18 * (20 * month + day + 1), :]
    print(sample)
    month_data[month] = sample

    x = np.empty([471 * 12, 18 * 9], dtype=float)
    y = np.empty([471 * 12, 1], dtype=float)

for month in range(12):
    for day in range(20):
        for hour in range(24):
            if day == 19 and hour > 14:
                continue
            x[471 * month + 24 * day + hour, :] = month_data[month][:,
                                                  24 * day + hour: 24 * day + hour + 9].reshape(1, -1)
            y[471 * month + 24 * day + hour, 0] = month_data[month][9, day * 24 + hour + 9]
print(x)

x_mean = np.mean(x, axis=0)  # 471 * 12
x_std = np.mean(x, axis=0)  # 18 * 9

for i in range(len(x)):
    for j in range(len(x[0])):
        if x[i][j] != 0:
            x[i][j] = (x[i][j] - x_mean[j]) / x_std[j]
dim = 18 * 9 + 1

w = np.zeros([dim, 1])
x = np.concatenate((np.ones([471 * 12, 1]), x), axis=1).astype(float)

learning_rate = 100
iter_time = 20000
adagrad = np.zeros([dim, 1])
eps = 0.0000000001

for t in range(iter_time):
    # loss = np.sqrt( np.sum( np.power( np.dot(x,w) - y , 2)) / 471 / 12)
    loss = np.sqrt(np.sum(np.power(np.dot(x, w) - y, 2)) / 471 / 12)
    if (t % 100 == 0):
        print(str(t) + ":" + str(loss))
    gradient = 2 * np.dot(x.transpose(), np.dot(x, w) - y)
    adagrad += gradient ** 2

    w = w - learning_rate * gradient / np.sqrt(adagrad + eps)


print(loss)