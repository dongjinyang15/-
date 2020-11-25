import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

x_list = np.empty([471 * 12, 9])
y_list = np.empty([471 * 12, 1])

x_train = np.empty([4500, 9 + 1])
x_val = np.empty([471 * 12 - 4500, 9 + 1])

y_train = np.empty([4500, 1])
y_val = np.empty([471 * 12 - 4500, 1])

wias = 0.01 * np.random.normal(size=(9 + 1, 1))

x_test = np.empty([240, 9])
ans = np.empty([240, 1])


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
            sample[:, day * 24: (day + 1) * 24] = train[18 * (day + 20 * month): 18 * (day + 20 * month + 1), :]

        month_data[month] = sample
    # print(month_data)
    for month in range(12):
        for i in range(480 - 9):
            x_list[471 * month + i, :] = month_data[month][9, i: i + 9].reshape(1, -1)
            y_list[471 * month + i] = month_data[month][9, i + 9]
    print(x_list)
    print(y_list)
    return x_list, y_list


def train_model(x_list, y_list, wias):
    # adagrad

    learning_rate = 0.1
    x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
    # print(x)
    data = np.concatenate((x, y_list), axis=1)
    epoch = 1500
    bats = 10
    x_train = x[:4500, :]
    y_train = y_list[:4500, :]
    # print(len(x_train))
    # print(x_train)
    x_val = x[4500:, :]
    # print(x_val)
    y_val = y_list[4500:, :]
    # print(y_val)
    adagrad = np.zeros([9 + 1, 1])
    for t in range(epoch):
        for bat in range(bats):
            data_x = x_train[bat * 450:(bat + 1) * 450, :]
            data_label = y_train[bat * 450:(bat + 1) * 450, :]
            data_label = np.array(data_label).reshape(-1, 1)
            # print(data_label)
            loss = np.sqrt(np.sum(np.power(np.dot(data_x, wias) - data_label, 2)) / 471)
            gradient = 2 * np.dot(data_x.transpose(), np.dot(data_x, wias) - data_label)
            adagrad += gradient ** 2
            wias -= learning_rate * gradient / np.sqrt(adagrad)
        print(loss)
    print(np.dot(x, wias) - y_list)
    print(wias)
    return x_list, wias, x_val, y_val


def test(x_list, y_list, wias):
    x = np.concatenate((np.ones([471 * 12, 1]), x_list), axis=1)
    x_val = x[4500:, :]
    # print(x_val)
    y_val = y_list[4500:, :]
    y_hat = np.dot(x_val, wias)
    plt.plot(y_hat)
    plt.plot(y_val)
    plt.show()


def show(wias):
    test1 = pd.read_csv('test.csv', encoding='BIG5')
    test1 = np.array(test1.iloc[:, 2:])
    for i in range(test1.shape[0]):
        for j in range(test1.shape[1]):
            if test1[i, j] != 'NR':
                test1[i, j] = float(test1[i, j])
            else:
                test1[i, j] = 0

    ans1 = pd.read_csv('ans.csv', encoding='BIG5')
    ans1 = np.array(ans1.iloc[:, 1:])
    for i in range(ans1.shape[0]):
        for j in range(ans1.shape[1]):
            ans1[i, j] = float(ans1[i, j])

    ans = ans1.copy()

    for i in range(240):
        x_test[i, :] = test1[i * 18 + 9, :].reshape(1, -1)
        print(x_test[i])
    x = np.concatenate((np.ones([240, 1]), x_test), axis=1)
    y = np.dot(x, wias)
    plt.plot(y)
    plt.plot(ans)
    print(y - ans)
    plt.show()


data_process(x_list, y_list)
train_model(x_list, y_list, wias)
test(x_list, y_list, wias)
show(wias)


