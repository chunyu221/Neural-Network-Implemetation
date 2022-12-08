import numpy as np
import matplotlib.pyplot as plt

# 設定
from os import path

txt_path = input("輸入路徑：")
# learn rate
lr = input("輸入學習率 = ")
lr = float(lr)
# lr = 0.05
N = input("收斂條件次數 = ")
# N = 1000

w = []
x_train = []
x_test = []
d_train = []
d_test = []

w = [float(input("w0 = "))]
w.append(float(input("w1 = ")))
w.append(float(input("w2 = ")))
# w = [1, 0, 0]

# 處理 dataset
def Dataset():
    # path = 'NN_HW1_DataSet/perceptron1.txt'
    x_max = -10000
    x_min = 10000
    d_max = -10000
    d_min = 10000
    with open(txt_path) as file:
        cnt = 0
        for line in file.readlines():
            line = line.strip()
            s = line.split(' ')

            if (cnt % 3 == 2):
                x_test.append([-1, float(s[0]), float(s[1])])
                d_test.append(int(s[2]))
                if (float(s[0]) > x_max):
                    x_max = float(s[0])
                if (float(s[0]) < x_min):
                    x_min = float(s[0])
                if (int(s[2]) > d_max):
                    d_max = int(s[2])
                if (int(s[2]) < d_min):
                    d_min = int(s[2])
            else:
                x_train.append([-1, float(s[0]), float(s[1])])
                d_train.append(int(s[2]))
                if (float(s[0]) > x_max):
                    x_max = float(s[0])
                if (float(s[0]) < x_min):
                    x_min = float(s[0])
                if (int(s[2]) > d_max):
                    d_max = int(s[2])
                if (int(s[2]) < d_min):
                    d_min = int(s[2])
            cnt+=1

    # 標準化 d
    for i in range(0, len(d_train)):
        d_train[i] = int((d_train[i] - d_min) / (d_max - d_min))
    for i in range(0, len(d_test)):
        d_test[i] = int((d_test[i] - d_min) / (d_max - d_min))

    return x_min, x_max
        
# summation
def Summation(num, type):
    v = 0
    if (type == 'train'):
        for i in range(0, 3):
            v += w[i] * x_train[num][i]
#         print(v)
    else:
        for i in range(0, 3):
            v += w[i] * x_test[num][i]
#         print(v)
    return v

# sign function
def Sign(v):
    if (v >= 0):
        return 1
    else:
        return 0     

# 修正鍵結值
def Modify(num, y, d):
    if (y == d):
        return True
    elif (y == 1 and d == 0):
#         print('1')
        for i in range(0, 3):
            w[i] = w[i] - lr * x_train[num][i]
    elif (y == 0 and d == 1):
#         print('2')
        for i in range(0, 3):
            w[i] = w[i] + lr * x_train[num][i]
    return False

# 畫圖
def Graph(s):
    x1 = np.array([])
    x2 = np.array([])
    x3 = np.array([])
    x4 = np.array([])
    if (s == 'test'):
        for i in range(0, len(x_test)):
            if (d_test[i] == 1):
                x1 = np.append(x1, x_test[i][1])
                x2 = np.append(x2, x_test[i][2])
#                 print(x_test[i][1], x_test[i][2], d_test[i])
            else:
                x3 = np.append(x3, x_test[i][1])
                x4 = np.append(x4, x_test[i][2])
#                 print(x_test[i][1], x_test[i][2], d_test[i])

        plt.plot(x1, x2, 'rx')
        plt.plot(x3, x4, 'bo')

        if (w[2] != 0):
            x = np.arange(x_min-1, x_max+2)
            y = (-1)*(w[1]/w[2])*x + w[0]/w[2]
            plt.plot(x, y)
        else:
            plt.axvline(x = (-1)*(w[0]/w[1]))

        plt.grid(True)
        plt.show()
    
    else:
        for i in range(0, len(x_train)):
            if (d_train[i] == 1):
                x1 = np.append(x1, x_train[i][1])
                x2 = np.append(x2, x_train[i][2])
            else:
                x3 = np.append(x3, x_train[i][1])
                x4 = np.append(x4, x_train[i][2])

        plt.plot(x1, x2, 'rx')
        plt.plot(x3, x4, 'bo')

        if (w[2] != 0):
            x = np.arange(x_min-1, x_max+2)
            y = (-1)*(w[1]/w[2])*x + w[0]/w[2]
            plt.plot(x, y)
        else:
            plt.axvline(x = (-1)*(w[0]/w[1]))

        plt.grid(True)
        plt.show()

# main
x_min, x_max = Dataset()

# training
correct = 0
all = 0
while (all != int(N)):
    for i in range(0, len(x_train)):
        all += 1
        v = Summation(i, 'train')
        y = Sign(v)
        if(Modify(i, y, d_train[i])):
            correct += 1
        if (i == len(x_train)-1):
            i = 0
        if (all == int(N)):
            break

        
print('\n訓練結果')
print('正確次數：{}'.format(correct), '總次數：{}'.format(all))
print('正確率：{}%'.format(correct/all*100), '\n')

Graph('train')

# testing
correct = 0
all = len(x_test)
for i in range(0, len(x_test)):
    v = Summation(i, 'test')
    y = Sign(v)
    if (y == d_test[i]):
        correct += 1
print('測試結果')
print('正確次數：{}'.format(correct), '總次數：{}'.format(all))
print('正確率：{}%'.format(correct/all*100), '\n')

# graph
Graph('test')

print("最終鍵結值")
print('w0 =', w[0])
print('w1 =', w[1])
print('w2 =', w[2])
print('learning rate =', lr)