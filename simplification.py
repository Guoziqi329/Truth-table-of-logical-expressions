import sympy as sym
from draw import is_only_alphabets, parse_logic_expression
import tkinter.messagebox as message


def Logical_expressions_are_simplified(expression):
    variables = []
    for i in range(len(expression)):
        for j in range(len(expression[i])):
            if is_only_alphabets(expression[i][j]) and (expression[i][j] not in variables):
                variables.append(expression[i][j])
    print(' '.join(variables))
    # 定义逻辑变量
    sym.symbols(' '.join(variables))

    # 化简表达式
    simplified_expr = sym.simplify_logic(expression)

    # 打印化简后的表达式
    print("化简后的表达式：", simplified_expr)

    return simplified_expr


def transform_expressions(list_of_expressions):
    n = 0
    for c in list_of_expressions:
        if c is '&':
            list_of_expressions[n] = ''
        if c is '|':
            list_of_expressions[n] = '+'
        n = n + 1


def Functional_simplification(Str_input):
    try:
        Str_input = parse_logic_expression(list(Str_input))
        Simplified_expressions = Logical_expressions_are_simplified(Str_input)
        Simplified_expressions_list = list(str(Simplified_expressions))
        transform_expressions(Simplified_expressions_list)
        print(''.join(Simplified_expressions_list))
        message.showinfo("函数表达式",
                         f"此化简不一定正确，请仔细确认（'~'代表非）\n化简后的表达式：{''.join(Simplified_expressions_list)}")
    except Exception as e:
        message.showerror("ERROR!", e)
