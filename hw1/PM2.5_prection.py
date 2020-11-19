import numpy as np
import pandas as pd
import math
x_list = np.empty([471*12, 9*18])
y_list = np.empty([471*12, 1])
wias = 0.01 * np.random.normal(size=(18*9+1, 1))

def data_process(x_list, y_list):
    month_data = {}
    train = pd.read_csv('train.csv', encoding='Big5')
    train = np.array(train.iloc[:, 3:])
    for i in range(train.shape[0]):
        for j in range(train.shape[1]):
            if train[i, j] != 'NR':
                train[i, j] = float(train[i, j])
            else:
                train[i, j] = 0
    # print(train)
    for month in range(12):
        sample = np.empty([18, 480])
        for day in range(20):
            sample[:, day*24 : (day+1)*24] = train[18*(day+20*month): 18*(day+20*month+1), :]

        month_data[month] = sample
    # print(month_data)
    for month in range(12):
        for i in range(480-9):
            x_list[471*month+i, :] = month_data[month][:, i: i+9].reshape(1, -1)
            y_list[471*month+i] = month_data[month][9, i+9]

    # print(x_list)
    # print(y_list)

    return x_list, y_list


def get_train_model(x_list):
    # 归一化
    x_mean = np.mean(x_list, axis=0)
    x_std = np.mean(x_list, axis=0)
    # print(len(x_list))
    for i in range(len(x_list)):
        for j in range(18*9):
            if x_list[i][j] != 0:
                x_list[i][j] = (x_list[i][j] - x_mean[j])/x_std[j]
    return x_list


def train_model(x_list, y_list, wias):
    # adagrad

    # wias = 0.01 * np.ones([18 * 9 + 1, 1])
    learning_rate = 0.1
    x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
    # print(x)
    data = np.concatenate((x, y_list), axis=1)

    # data = np.random.permutation(data)

    epoch = 1000
    bats = 11
    adagrad = np.zeros([18 * 9 + 1, 1])
    for t in range(epoch):
        for bat in range(bats):
            data_x = x[bat * 471:(bat + 1) * 471, :]
            data_label = y_list[bat * 471:(bat + 1) * 471, :]
            data_label = np.array(data_label).reshape(-1, 1)
            # print(data_label)
            loss = np.sqrt(np.sum(np.power(np.dot(data_x, wias) - data_label, 2))/471)
            gradient = 2 * np.dot(data_x.transpose(), np.dot(data_x, wias) - data_label)
            adagrad += gradient ** 2
            wias = wias - learning_rate * gradient / np.sqrt(adagrad)
        print(loss)
    # print(loss)
    # print(wias)
    # print(np.dot(x, wias)-y_list)
    print(np.dot(x, wias)-y_list)
    print(wias)
    return x_list, wias


'''
def train_model1(x_list, y_list, wias):

    learning_rate = 0.01
    x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
    epoch = 10000
    adagrad = np.zeros([18 * 9 + 1, 1])
    for t in range(epoch):
        loss = np.sqrt(np.sum(np.power(np.dot(x, wias) - y_list, 2))/471/12)
        gradient = 2 * np.dot(x.transpose(), np.dot(x, wias) - y_list)
        adagrad += gradient ** 2
        wias = wias - learning_rate * gradient / np.sqrt(adagrad)
        if t % 100 == 0:
            print(loss)
    # print(loss)
    # print(wias)

    return x_list, wias
'''


def test(x_list, y_list, wias):
    print(wias)
    x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
    data_label = y_list[0 * 471:(0 + 1) * 471, 0]
    print(data_label)
    data_x = x[0 * 471:(0 + 1) * 471, 0:]
    print(data_x[0])
    data_label = np.array(data_label).reshape(-1, 1)
    loss = np.dot(data_x, wias) - data_label
    sum = np.sum(loss**2)/471
    # print(data_label)
    # print(np.dot(data_x, wias))
    # print(len(data_label))
    # print(len(loss))
    # print(loss)
    # print(sum)

data_process(x_list, y_list)
print(wias)
train_model(x_list, y_list, wias)
print(wias)
x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
data_label = y_list[0 * 471:(0 + 1) * 471, 0]
data_x = x[0 * 471:(0 + 1) * 471, 0:]
data_label = np.array(data_label).reshape(-1, 1)
loss = np.dot(data_x, wias) - data_label
# sum = np.sum(loss**2)/471
# print(loss)
# test(x_list, y_list, wias)