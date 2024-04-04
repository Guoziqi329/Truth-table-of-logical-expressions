from tkinter import ttk
from draw import *
from simplification import *

if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('500x250')
    root.title('逻辑函数计算器')
    root.resizable(False, False)

    notebook = ttk.Notebook(root)
    notebook.pack(pady=5, expand=True)

    frame1 = ttk.Frame(notebook, width=490, height=290)
    frame2 = ttk.Frame(notebook, width=490, height=290)
    frame3 = ttk.Frame(notebook, width=490, height=290)

    frame1.pack(fill='both', expand=True)
    frame2.pack(fill='both', expand=True)
    frame3.pack(fill='both', expand=True)

    notebook.add(frame1, text='单返回逻辑函数画图')
    notebook.add(frame2, text='多返回逻辑函数画图')
    notebook.add(frame3, text='函数化简')

    # 单返回逻辑函数
    label = tk.Label(frame1, text="请输入逻辑函数：")
    label.place(x=60, y=40)
    entry = tk.Entry(frame1, width=30)
    entry.place(x=170, y=40)
    start_button = tk.Button(frame1, text="开始", command=lambda: start_button_clicked(entry))
    start_button.place(x=240, y=90)

    # 多返回逻辑函数计算
    label1 = tk.Label(frame2, text="请输入表达式的个数：")
    label1.place(x=120, y=40)
    entry1 = tk.Entry(frame2, width=10)
    entry1.place(x=250, y=40)
    start_button1 = tk.Button(frame2, text="开始", command=lambda: Multi_function_input_interface(entry1.get()))
    start_button1.place(x=240, y=90)

    # 函数化简
    label2 = tk.Label(frame3, text="请输入要化简的表达式:")
    label2.place(x=50, y=40)
    entry2 = tk.Entry(frame3, width=30)
    entry2.place(x=190, y=40)
    start_button2 = tk.Button(frame3, text="开始", command=lambda: Functional_simplification(entry2.get()))
    start_button2.place(x=240, y=90)
    root.mainloop()
