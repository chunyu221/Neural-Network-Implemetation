from tkinter.constants import LEFT
import numpy as np
import tkinter as tk
# import matplotlib.pyplot as plt

# txt_path = input("輸入路徑：")
# train_path = "./basic_Training.txt"
# test_path = "./basic_Testing.txt"

# data_num = 3
# x_row = 12
# x_col = 9
# n = 100
# train_x = np.zeros((data_num, x_row*x_col), dtype=np.int32)
# input_x = np.zeros((data_num, x_row*x_col), dtype=np.int32)
# output_x = np.zeros((data_num, x_row*x_col), dtype=np.int32)

# W = np.array([[], []], dtype=np.float64)
# bias = np.array([], dtype=np.float64)

def showFile(path):
    with open(path) as file:
        string = file.read()  
        file.close()  

    return string

def result():
    window2 = tk.Toplevel(window)
    window2.title("Result")
    result_label = tk.Label(window2,
                        text=showFile("./output.txt"),
                        justify=LEFT,
                        width=30)
    result_label.pack()

def readFile(path, data_num, x_row, x_col):
    x = np.zeros((data_num, x_row*x_col), dtype=np.int32)
    with open(path) as file:
        row = 0
        col = 0
        for line in file.readlines():
            if (line == '\n'):
                row += 1
                col = 0
            else:
                for i in line:
                    if (i == '\n'):
                        continue
                    if (i == '1'):
                        x[row][col] = 1
                    else:
                        x[row][col] = -1
                    col += 1       
        file.close()

    return x

def createW(train_x, x_row, x_col):
    w = np.zeros((x_row*x_col, x_row*x_col))
    _bias = np.array([], dtype=np.float64)
    for i in train_x:
        temp = np.zeros((x_row*x_col, x_row*x_col))
        for j in range(0, x_row*x_col):
            for k in range(0, x_row*x_col):
                temp[j][k] = i[j]*i[k]

        w = np.add(w, temp)

    for i in range(0, x_row*x_col):
        w[i][i] = 0

    w = np.divide(w, x_row*x_col)
    
    _bias = np.sum(w, axis=0)

    return w, _bias

def recall(in_x, w, _bias, data_num, x_row, x_col):
    out_x = np.zeros((data_num, x_row*x_col))
    out_x_int = np.zeros((data_num, x_row*x_col), dtype=np.int32)
    for i in range(0, data_num):
        for j in range(0, x_row*x_col):
            for k in range(0, x_row*x_col):
                out_x[i][j] += w[j][k] * in_x[i][k]
            out_x[i][j] -= _bias[j]

            # print(out_x[k][i], ' ', in_x[k][i])
            if (out_x[i][j] > 0):
                out_x_int[i][j] = 1
                # print("1")
            elif (out_x[i][j] < 0):
                out_x_int[i][j] = -1
                # print("-1")
            else:
                out_x_int[i][j] = in_x[i][j]
                # print("0")
            # if (out_x_int[i][j] != in_x[i][j]):
            #     print("change")

    return out_x_int

def writeFile(output_x, output_path, x_row, x_col):
    string = ""
    f = open(output_path, 'w')
    for i in output_x:
        cnt = 0
        for j in range(0, x_row):
            string = ""
            for k in range(0, x_col):
                if (i[cnt] == 1):
                    string += str(i[cnt])
                else:
                    string += ' '
                cnt += 1
            string += '\n'
            # print(cnt)
            f.write(string)
        # print("end")
        f.write('\n')
    f.close()
    
def train():
    train_path = train_entry.get()
    x_row = int(row_entry.get())
    x_col = int(col_entry.get())
    data_num = int(num_entry.get())
    print(x_row, x_col, data_num)
    if (train_path != ""):
        print(train_path)
        # train
        train_x = readFile(train_path, data_num, x_row, x_col)
        # print(train_x)
        W, bias = createW(train_x, x_row, x_col)
        print(W)
        # np.savetxt("weight.txt", W)
        print(bias)


    test_path = test_entry.get()
    # test
    input_x = readFile(test_path, data_num, x_row, x_col)
    # print(input_x)
    output_x = recall(input_x, W, bias, data_num, x_row, x_col)
    # writeFile("./outputfile.txt")

    # for i in range(0, n):
    #     output_x = recall(output_x)
    # print(output_x)
    writeFile(output_x, "./output.txt", x_row, x_col)
    
    result()

    return output_x
    

if __name__ == '__main__':
    window = tk.Tk()

    window.title("Hopfield")
    window.geometry("300x200")

    set_frame = tk.Frame(window)
    set_frame.pack(side=tk.TOP)
    row_label = tk.Label(set_frame, 
                            text="row: ",
                            height=3)
    row_label.pack(side=tk.LEFT)
    row_entry = tk.Entry(set_frame,
                        width=3)
    row_entry.pack(side=tk.LEFT)
    col_label = tk.Label(set_frame, 
                            text="col: ",
                            height=3)
    col_label.pack(side=tk.LEFT)
    col_entry = tk.Entry(set_frame,
                        width=3)
    col_entry.pack(side=tk.LEFT)
    num_label = tk.Label(set_frame, 
                            text="number: ",
                            height=3)
    num_label.pack(side=tk.LEFT)
    num_entry = tk.Entry(set_frame,
                        width=3)
    num_entry.pack(side=tk.LEFT)

    train_frame = tk.Frame(window)
    train_frame.pack(side=tk.TOP)
    train_label = tk.Label(train_frame, 
                            text="Training data path: ", 
                            width=15, 
                            height=3)
    train_label.pack(side=tk.LEFT)
    train_entry = tk.Entry(train_frame)
    train_entry.pack(side=tk.LEFT)

    test_frame = tk.Frame(window)
    test_frame.pack(side=tk.TOP)
    test_label = tk.Label(test_frame, 
                            text="Testing data path: ", 
                            width=15,
                            height=3)
    test_label.pack(side=tk.LEFT)
    test_entry = tk.Entry(test_frame)
    test_entry.pack(side=tk.LEFT)

    train_btn = tk.Button(window, text="train", command=train)
    train_btn.pack()

    window.mainloop()

    print("end")