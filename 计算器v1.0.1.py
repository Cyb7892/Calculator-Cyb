import tkinter as tk
from tkinter import font
import math
from fractions import Fraction

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
        self.fraction_font = font.Font(family="SimHei", size=12)
        
        # 初始化表达式变量
        self.expression = ""
        self.current_input = ""
        self.is_fraction = False  # 标记是否正在输入分数
        self.numerator = ""       # 分子
        self.denominator = ""     # 分母
        self.fraction_result = ""  # 存储分数形式结果
        
        # 创建UI
        self.create_widgets()
        
        # 绑定键盘事件
        self.bind_keyboard_events()
    
    def create_widgets(self):
        # 创建显示区域
        self.display_frame = tk.Frame(self.root, bg="#f0f0f0", height=120)
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
        
        # 分数结果显示（仅在需要时显示）
        self.fraction_var = tk.StringVar()
        self.fraction_label = tk.Label(
            self.display_frame, 
            textvariable=self.fraction_var, 
            font=self.fraction_font,
            bg="#f0f0f0", 
            fg="#888888",
            anchor=tk.E
        )
        self.fraction_label.pack(fill=tk.BOTH, expand=True)
        
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
            ['π', '0', '.', '='],
            ['/', '', '', '']  # 分数按钮
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
                elif button_text in ['C', '←', '±', 'π', '/']:
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
        for i in range(6):
            self.buttons_frame.grid_rowconfigure(i, weight=1)
    
    def bind_keyboard_events(self):
        """绑定键盘事件"""
        # 数字键
        for key in '0123456789':
            self.root.bind(key, lambda e, k=key: self.on_button_click(k))
        
        # 运算符
        self.root.bind('+', lambda e: self.on_button_click('+'))
        self.root.bind('-', lambda e: self.on_button_click('-'))
        self.root.bind('*', lambda e: self.on_button_click('×'))
        self.root.bind('/', lambda e: self.on_button_click('÷'))
        
        # 其他功能键
        self.root.bind('.', lambda e: self.on_button_click('.'))
        self.root.bind('<Return>', lambda e: self.on_button_click('='))
        self.root.bind('<BackSpace>', lambda e: self.on_button_click('←'))
        self.root.bind('c', lambda e: self.on_button_click('C'))
        self.root.bind('C', lambda e: self.on_button_click('C'))
        self.root.bind('%', lambda e: self.on_button_click('/'))  # 用%键作为分数输入
        self.root.bind('<Escape>', lambda e: self.on_button_click('C'))  # ESC键清空数据
        
    def on_button_click(self, text):
        """处理按钮点击事件"""
        # 清除分数显示（除了等号和清除键）
        if text not in ['=', 'C']:
            self.fraction_var.set("")
            self.fraction_result = ""
            
        if text.isdigit() or text == '.':
            # 数字或小数点
            if text == '.' and '.' in self.current_input:
                return  # 防止多个小数点
                
            # 处理分数输入
            if self.is_fraction:
                if not self.numerator:  # 还没有输入分子
                    self.numerator += text
                    self.current_input = f"{self.numerator}/"
                else:  # 已经输入分子，正在输入分母
                    self.denominator += text
                    self.current_input = f"{self.numerator}/{self.denominator}"
            else:
                self.current_input += text
                
            self.current_var.set(self.current_input)
            
        elif text in ['+', '-', '×', '÷']:
            # 运算符
            # 如果正在输入分数，先计算分数值
            if self.is_fraction and self.numerator and self.denominator:
                self.calculate_fraction()
                
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
            # 如果正在输入分数，先计算分数值
            if self.is_fraction and self.numerator and self.denominator:
                self.calculate_fraction()
            self.calculate_result()
            
        elif text == 'C':
            # 清除所有
            self.expression = ""
            self.current_input = ""
            self.numerator = ""
            self.denominator = ""
            self.is_fraction = False
            self.fraction_result = ""
            self.expression_var.set("")
            self.current_var.set("")
            self.fraction_var.set("")
            
        elif text == '←':
            # 退格
            if self.current_input:
                self.current_input = self.current_input[:-1]
                # 更新分数相关变量
                if '/' in self.current_input:
                    parts = self.current_input.split('/', 1)
                    self.numerator = parts[0]
                    self.denominator = parts[1] if len(parts) > 1 else ""
                    self.is_fraction = True
                else:
                    self.numerator = self.current_input
                    self.denominator = ""
                    self.is_fraction = bool(self.numerator and not self.current_input)
                self.current_var.set(self.current_input)
            
        elif text == '±':
            # 正负号转换
            if self.current_input:
                if self.current_input.startswith('-'):
                    self.current_input = self.current_input[1:]
                else:
                    self.current_input = '-' + self.current_input
                self.current_var.set(self.current_input)
                
        elif text == 'π':
            # 插入π值(保留两位小数)
            pi_value = "3.14"
            self.current_input += pi_value
            self.current_var.set(self.current_input)
            
        elif text == '/':
            # 分数输入
            if not self.is_fraction and self.current_input:
                # 如果不在分数模式且已有输入，将当前输入设为分子
                self.numerator = self.current_input
                self.is_fraction = True
                self.current_input += "/"
                self.current_var.set(self.current_input)
            elif self.is_fraction and self.denominator:
                # 如果已完成分数输入，计算分数值
                self.calculate_fraction()
    
    def calculate_fraction(self):
        """计算分数值"""
        try:
            num = float(self.numerator)
            den = float(self.denominator)
            if den == 0:
                self.current_var.set("错误(除数为0)")
                self.current_input = ""
            else:
                result = num / den
                # 处理整数结果
                if result.is_integer():
                    result = int(result)
                self.current_input = str(result)
                self.current_var.set(self.current_input)
        except Exception as e:
            self.current_var.set("错误")
            self.current_input = ""
        finally:
            # 重置分数状态
            self.is_fraction = False
            self.numerator = ""
            self.denominator = ""
    
    def is_infinite_decimal(self, value):
        """判断一个数是否为无限小数"""
        try:
            # 尝试将浮点数转换为分数
            frac = Fraction(value).limit_denominator()
            denominator = frac.denominator
            
            # 检查分母是否只包含2和5的因数（有限小数的特征）
            while denominator % 2 == 0:
                denominator //= 2
            while denominator % 5 == 0:
                denominator //= 5
                
            # 如果化简后分母为1，则是有限小数
            return denominator != 1
        except:
            return False
    
    def calculate_result(self):
        """计算表达式结果，并在无限小数时显示最简分数"""
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
                    self.current_input = str(result)
                    self.current_var.set(self.current_input)
                else:
                    # 检查是否为无限小数
                    self.current_input = str(result)
                    self.current_var.set(self.current_input)
                    
                    # 如果是无限小数，显示最简分数
                    if isinstance(result, float) and self.is_infinite_decimal(result):
                        frac = Fraction(result).limit_denominator()
                        self.fraction_result = f"{frac.numerator}/{frac.denominator}"
                        self.fraction_var.set(f"分数形式: {self.fraction_result}")
                
                self.expression = ""
                self.expression_var.set("")
                
            except Exception as e:
                self.current_var.set("错误")
                self.current_input = ""

if __name__ == "__main__":
    root = tk.Tk()
    app = Calculator(root)
    root.mainloop()
    