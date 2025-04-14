from UI import *
import sys
from PyQt6 import QtWidgets
from Twincat_UI import *
from PyQt6 import QtCore, QtGui, QtWidgets
import pyads
from ctypes import sizeof
import time
import configparser
from AutoTK import *
from PyQt6.QtCore import QTimer
from PyQt6.QtCore import QThread, pyqtSignal
from UI import  *
import time
import pyads
from PyQt6.QtCore import QThread

class Testcase_1(QThread):
    def __init__(self, ui):
        super().__init__()
        self.ui = ui
        
        # 列表格式: 每个元素是 ((符号名, 数据类型), 值)
        self.symbol_and_values = [
            (("MAIN.Enable1", pyads.PLCTYPE_BOOL), False),
            (("MAIN.Enable2", pyads.PLCTYPE_BOOL), False),
            (("MAIN.Enable3", pyads.PLCTYPE_BOOL), False)
        ]
        
        start_time = time.perf_counter()
        self.next_call = [start_time, start_time, start_time]

    def run(self):
        while self.ui.PB_Start_1.isChecked():
            current_time = time.perf_counter()

            for i in range(3):
                if self.ui.CH_Active[0][i] and current_time >= self.next_call[i]:
                    old_val = self.get_list_value(self.symbol_and_values, CH_E[i], pyads.PLCTYPE_BOOL)
                    if old_val is not None:
                        new_val = not old_val
                        self.set_list_value(self.symbol_and_values, CH_E[i], pyads.PLCTYPE_BOOL, new_val)
                        self.next_call[i] = current_time + self.ui.CH_Interval[0][i]

            self.ui.plc.write_list_by_name(self.symbol_and_values)
            time.sleep(0.01)

    def get_list_value(self, lst, symbol_name: str, plc_type):

        for (sym_t, val) in lst:
            sym, t = sym_t
            if sym == symbol_name and t == plc_type:
                return val
        return None

    def set_list_value(self, lst, symbol_name: str, plc_type, new_val):

        for idx, (sym_t, old_val) in enumerate(lst):
            sym, t = sym_t
            if sym == symbol_name and t == plc_type:
                lst[idx] = ((sym, t), new_val)
                return



        

            


class Testcase_2(QThread):
    def __init__(self,ui):
        super().__init__()
        self.ui = ui
    def run(self):
        while(self.ui.PB_Start_2.isChecked()==True):
            
            print("GOOD")
            time.sleep(0.1)