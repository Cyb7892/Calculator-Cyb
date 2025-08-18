import tkinter as tk
from tkinter import font

class Calculator:
    def __init__(self, root):
        # 设置窗口标题和基本属性
        self.root = root
        self.root.title("计算器")
        self.root.resizable(False, False)  # 禁止窗口大小调整
        self.root.configure(bg="#f0f0f0")  # 设置背景色
        
        # 设置字体
        self.display_font = font.Font(family="SimHei", size=20)
        self.button_font = font.Font(family="SimHei", size=14)
        
        # 初始化表达式变量
        self.expression = ""
        self.current_input = ""
        
        # 创建UI
        self.create_widgets()
    
    def create_widgets(self):
        # 创建显示区域
        self.display_frame = tk.Frame(self.root, bg="#f0f0f0", height=100)
        self.display_frame.pack(fill=tk.BOTH, padx=5, pady=5)
        
        # 表达式显示
        self.expression_var = tk.StringVar()
        self.expression_label = tk.Label(
            self.display_frame, 
            textvariable=self.expression_var, 
            font=font.Font(family="SimHei", size=12),
            bg="#f0f0f0", 
            fg="#666666",
            anchor=tk.E,
            wraplength=280
        )
        self.expression_label.pack(fill=tk.BOTH, expand=True)
        
        # 当前输入显示
        self.current_var = tk.StringVar()
        self.current_label = tk.Label(
            self.display_frame, 
            textvariable=self.current_var, 
            font=self.display_font,
            bg="#f0f0f0", 
            fg="#333333",
            anchor=tk.E
        )
        self.current_label.pack(fill=tk.BOTH, expand=True)
        
        # 创建按钮区域
        self.buttons_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.buttons_frame.pack(padx=5, pady=5)
        
        # 按钮布局
        button_layout = [
            ['C', '←', '±', '÷'],
            ['7', '8', '9', '×'],
            ['4', '5', '6', '-'],
            ['1', '2', '3', '+'],
            ['', '0', '.', '=']
        ]
        
        # 按钮颜色配置
        self.button_styles = {
            'number': {'bg': '#ffffff', 'fg': '#333333', 'relief': tk.RAISED, 'bd': 1},
            'operator': {'bg': '#ff9500', 'fg': '#ffffff', 'relief': tk.RAISED, 'bd': 1},
            'function': {'bg': '#e0e0e0', 'fg': '#333333', 'relief': tk.RAISED, 'bd': 1}
        }
        
        # 创建按钮
        for r, row in enumerate(button_layout):
            for c, button_text in enumerate(row):
                if button_text == '':  # 空按钮用于布局调整
                    continue
                
                # 确定按钮样式
                if button_text in ['+', '-', '×', '÷', '=']:
                    style = self.button_styles['operator']
                elif button_text in ['C', '←', '±']:
                    style = self.button_styles['function']
                else:
                    style = self.button_styles['number']
                
                # 创建按钮
                btn = tk.Button(
                    self.buttons_frame,
                    text=button_text,
                    font=self.button_font,
                    width=6,
                    height=2,
                    **style,
                    command=lambda text=button_text: self.on_button_click(text)
                )
                
                # 放置按钮
                btn.grid(row=r, column=c, padx=2, pady=2, sticky="nsew")
        
        # 调整网格权重，使按钮大小合适
        for i in range(4):
            self.buttons_frame.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
    
    def on_button_click(self, text):
        """处理按钮点击事件"""
        if text.isdigit() or text == '.':
            # 数字或小数点
            if text == '.' and '.' in self.current_input:
                return  # 防止多个小数点
            self.current_input += text
            self.current_var.set(self.current_input)
            
        elif text in ['+', '-', '×', '÷']:
            # 运算符
            if self.current_input:
                if self.expression:
                    # 如果已有表达式，先计算结果
                    self.calculate_result()
                    self.expression = self.current_input + text
                else:
                    self.expression = self.current_input + text
                self.expression_var.set(self.expression)
                self.current_input = ""
                self.current_var.set("")
                
        elif text == '=':
            # 计算结果
            self.calculate_result()
            
        elif text == 'C':
            # 清除所有
            self.expression = ""
            self.current_input = ""
            self.expression_var.set("")
            self.current_var.set("")
            
        elif text == '←':
            # 退格
            self.current_input = self.current_input[:-1]
            self.current_var.set(self.current_input)
            
        elif text == '±':
            # 正负号转换
            if self.current_input:
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.current_var.set(self.current_input)
    
    def calculate_result(self):
        """计算表达式结果"""
        if self.expression and self.current_input:
            try:
                # 构建完整表达式
                full_expression = self.expression + self.current_input
                # 替换×和÷为Python可识别的*和/
                full_expression = full_expression.replace('×', '*').replace('÷', '/')
                
                # 计算结果
                result = eval(full_expression)
                
                # 处理整数结果显示
                if isinstance(result, float) and result.is_integer():
                    result = int(result)
                
                # 更新显示
                self.current_input = str(result)
                self.current_var.set(self.current_input)
                self.expression = ""
                self.expression_var.set("")
                
            except Exception as e:
                self.current_var.set("错误")
                self.current_input = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
    