import sympy as sym
import matplotlib.pyplot as plt
from plottable import Table, ColumnDefinition
import pandas as pd
import tkinter as tk
import tkinter.messagebox as message

def is_only_alphabets(str):
    if str.isalpha():
        return True
    else:
        return False

def offset(expression_str, n):
    i = 0
    while expression_str[n - 1] in ['~(', '<']:
        if (expression_str[n - 2] in ['|','&','~(']) or n < 2:
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
    Print_Array = pd.DataFrame(data=data, columns=variables+['Y']).round(2)
    Table(Print_Array,column_definitions=[ColumnDefinition(name="index", textprops={"ha": "center", "weight": "bold"}),
                                          ColumnDefinition(name=variables[0], border="l")])
    plt.savefig("table.jpg", dpi=400, bbox_inches='tight')
    plt.show()

def start_button_clicked():
     try:
        Str_input = list(entry.get())
        variables = []
        for i in range(len(Str_input)):
            if is_only_alphabets(Str_input[i]) and (Str_input[i] not in variables):
                variables.append(Str_input[i])
        expression_str = parse_logic_expression(Str_input)
        print(expression_str)
        evaluate_logic_expression(expression_str, variables)
     except Exception as e:
         message.showwarning("ERROR!", e)


if __name__ == '__main__':
    root = tk.Tk()
    root.title("函数真值表")
    root.geometry("500x200")

    label = tk.Label(root, text="请输入逻辑函数：")
    label.place(x=60, y=40)

    entry = tk.Entry(root, width=30)
    entry.place(x=170, y=40)


    start_button = tk.Button(root, text="开始", command=start_button_clicked)
    start_button.place(x=240, y=90)
    root.mainloop()
