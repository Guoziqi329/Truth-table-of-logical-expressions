import sympy as sym
import matplotlib.pyplot as plt
from plottable import Table, ColumnDefinition
import pandas as pd
import matplotlib
import tkinter.messagebox as message
import tkinter as tk

matplotlib.use('TkAgg')


def is_only_alphabets(Str):
    if Str.isalpha():
        return True
    else:
        return False


def offset(expression_str, n):
    i = 0
    while expression_str[n - 1] in ['~(', '<']:
        if (expression_str[n - 2] in ['|', '&', '~(']) or n < 2:
            return i
        i = i + 1
        n = n - 1
    return i


def parse_logic_expression(expression_str):
    n = 0
    while n < len(expression_str):
        s = expression_str[n]
        if s == '+':
            expression_str[n] = '|'
        if s == '*':
            expression_str[n] = '&'
        if n > 0 and is_only_alphabets(expression_str[n]):
            if is_only_alphabets(expression_str[n - 1]) or (expression_str[n - 1] in ['>', ')']):
                expression_str.insert(n, '&')
            o = offset(expression_str, n)
            if o > 0:
                expression_str.insert(n - o, '&')
                n = n + o
        if s == '<':
            if n > 0 and expression_str[n - 1] in ['>', ')']:
                expression_str.insert(n, '&')
                n = n + 1
                expression_str[n] = '~('
            else:
                expression_str[n] = '~('
        if s == '>':
            expression_str[n] = ')'
        n = n + 1
    return ''.join(expression_str)


def evaluate_logic_expression(expression_str, variables):
    symbols = [sym.Symbol(var) for var in variables]
    parsed_expr = sym.sympify(expression_str)
    header = "  ".join(variables + ["Result"])
    print("-" * len(header))

    data = []

    for assignment in sym.cartes([0, 1], repeat=len(variables)):
        values = {symbols[i]: assignment[i] for i in range(len(variables))}
        result = parsed_expr.subs(values)
        data.append([val for val in assignment + (result,)])

    for l in range(0, len(data)):
        for r in range(0, len(data[l])):
            if not data[l][r]:
                data[l][r] = 0
            if data[l][r]:
                data[l][r] = 1
    print(data)
    return data


def display_logic_expression(data, variables):
    Print_Array = pd.DataFrame(data=data, columns=variables + ['Y']).round(2)
    Table(Print_Array, column_definitions=[ColumnDefinition(name="index", textprops={"ha": "center", "weight": "bold"}),
                                           ColumnDefinition(name=variables[0], border="l")])
    plt.show()


def start_button_clicked(entry):
    try:
        Str_input = list(entry.get())
        variables = []
        for i in range(len(Str_input)):
            if is_only_alphabets(Str_input[i]) and (Str_input[i] not in variables):
                variables.append(Str_input[i])
        expression_str = parse_logic_expression(Str_input)
        print(expression_str)
        data = evaluate_logic_expression(expression_str, variables)
        display_logic_expression(data, variables)
    except Exception as e:
        message.showwarning("ERROR!", e)


def evaluate_logic_expression_Multi_formula(expression_str, variables):
    symbols = [sym.Symbol(var) for var in variables]
    parsed_expr = sym.sympify(expression_str)

    result_list = []
    data = []
    for assignment in sym.cartes([0, 1], repeat=len(variables)):
        values = {symbols[i]: assignment[i] for i in range(len(variables))}
        result = parsed_expr.subs(values)
        result_list.append(result)
        data.append([val for val in assignment])

    for i in range(len(result_list)):
        if not result_list[i]:
            result_list[i] = 0
        if result_list[i]:
            result_list[i] = 1

    return [data, result_list]


def display_logic_expression_multi_formula(data, variables, num):
    Print_Array = pd.DataFrame(data=data, columns=variables + [f'Y{n + 1}' for n in range(int(num))]).round(2)
    print(Print_Array)
    Table(Print_Array, column_definitions=[ColumnDefinition(name="index", textprops={"ha": "center", "weight": "bold"}),
                                           ColumnDefinition(name=variables[0], border="l")])
    plt.show()


def Multi_formula_calculation(expression, num):
    try:
        expression_list = []
        for i in range(len(expression)):
            expression_list.append(expression[i].get())

        Str_input_list = []
        for i in range(len(expression_list)):
            Str_input_list.append(list(expression_list[i]))

        variables = []
        for i in range(len(Str_input_list)):
            for j in range(len(Str_input_list[i])):
                if is_only_alphabets(Str_input_list[i][j]) and (Str_input_list[i][j] not in variables):
                    variables.append(Str_input_list[i][j])

        expression_list_Processed = []
        for expression in expression_list:
            expression_list_Processed.append(parse_logic_expression(list(expression)))
        print(expression_list_Processed)

        data_result = []
        for expression in expression_list_Processed:
            data_result.append(evaluate_logic_expression_Multi_formula(expression, variables))

        Enumerate_list = data_result[0][0]
        results_list = []
        for i in range(len(data_result)):
            results_list.append(data_result[i][1])

        for i in range(len(Enumerate_list)):
            for j in range(len(results_list)):
                n = results_list[j][i]
                Enumerate_list[i].append(n)

        if len(variables) >= 6:
            message.showwarning(title='您的变量太多', message='您的变量太多，无法画图,但已在终端显示')
            Print_Array = pd.DataFrame(data=Enumerate_list,
                                       columns=variables + [f'Y{n + 1}' for n in range(int(num))]).round(2)
            print(Print_Array)
            return 0

        display_logic_expression_multi_formula(Enumerate_list, variables, num)
    except Exception as e:
        message.showerror('ERROR!', e)


def Multi_function_input_interface(num):
    try:
        if num == 1:
            message.showinfo("数据错误", "一个逻辑函数请到第一个模块！")
            return 0
        root2 = tk.Tk()
        root2.title("请输入函数")
        root2.geometry("400x200")
        expression = {}
        for i in range(int(num)):
            expression[i] = tk.Entry(root2, width=30)
            expression[i].grid(row=i, column=1)
        Label_list = {}
        for i in range(int(num)):
            Label_list[i] = tk.Label(root2, text=f"请输入Y{i + 1}：")
            Label_list[i].grid(row=i, column=0)
        start_button = tk.Button(root2, text="开始", command=lambda: Multi_formula_calculation(expression, num))
        start_button.grid(row=int(num) + 1, column=1, sticky="w")
    except Exception as e:
        message.showerror("ERROR!", e)
