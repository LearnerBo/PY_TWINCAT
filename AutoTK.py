import pyautogui
import cv2
import numpy as np
import time
import tkinter as tk
from tkinter import filedialog, simpledialog
from tkinter import messagebox

class Auto_TK():
    def __init__(self):
        self.root = tk.Tk()
        self.root.withdraw()  # 隐藏主窗口
        self.root.attributes("-topmost",True)
        self.Path = None
        self.Password = "20250601"
        self.InputPassword = None


    def get_save_path(self):
        save_directory = filedialog.askopenfilename(title="请选择升级的HEX文件",filetypes=[("HEX Files", "*.hex"), ("All Files", "*.*")])
        if not save_directory:  
            return None
        self.Path = save_directory
        print(self.Path)
        return self.Path
    def root_password(self):
        if self.InputPassword != self.Password:
            self.InputPassword = simpledialog.askstring("输入密码", "Root密码:")
        if self.InputPassword == self.Password:
            # messagebox.showinfo("成功", "密码正确")
            return True
        elif self.InputPassword !=None:
            messagebox.showinfo("失败","密码错误")
            return False
        return False
    def ask_yes(self):
        result = messagebox.askyesno("确认升级", "请确保升级过程中不要断电,并耐心等待固件烧录")
        return result
    
    def burnprocess(self):
        messagebox.showinfo("恭喜你!","固件升级完成(〃'▽'〃)")
    
    def warinning_no_hex(self):
        messagebox.showinfo("缺少HEX文件","请选择HEX文件😠😠😠")

    def warinning(self,str):
        messagebox.showinfo("警告",str+"😠😠😠")
    
    def show(self,title,str):
        messagebox.showinfo(title,str)
    

if __name__ == "__main__":
    TK = Auto_TK()
    # TK.get_save_path()
    # TK.root_password()
    TK.ask_yes()