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
# AMS_ID = "192.168.1.2.1.1"
# IP_ADRESS = "127.0.0.1"
# PORT = 851
CH1_E = "MAIN.Enable1"
CH2_E = "MAIN.Enable2"
CH3_E = "MAIN.Enable3"
CH1_P = "MAIN.Polarity1"
CH2_P = "MAIN.Polarity2"
CH3_P = "MAIN.Polarity3"
CH1_V = "MAIN.Voltage1"
CH2_V = "MAIN.Voltage2"
CH3_V = "MAIN.Voltage3"
Config_file = "config.ini"
class UI_Twincat_Controller(QtWidgets.QMainWindow,Ui_Twincat_UI):
    def __init__(self,parent = None):
        super(UI_Twincat_Controller, self).__init__(parent)
        self.config = configparser.ConfigParser()
        self.config.read(Config_file)
        self.ams_net_id=self.config.get("config","ams_net_id")
        self.port = self.config.getint("config","port")
        self.ip_adress = self.config.get("config","ip_adress")
        self.tk = Auto_TK()
        self.setupUi(self)
        self.setupconnect()
        self.plc = pyads.Connection(self.ams_net_id,self.port,self.port)
        self.plc.open()

        self.interval_ms = [0] * 3
        self.step_volt = [0] * 3
        self.dir = [-1] * 3
        self.volt = [0] * 3

    def precise_sleep(self,seconds):
        start = time.perf_counter()
        while time.perf_counter() - start < seconds/1000:
            pass


    def setupconnect(self):
        self.PB_Enable_1.clicked.connect(self.slot_PB_Enable_1_clicked)
        self.PB_Enable_2.clicked.connect(self.slot_PB_Enable_2_clicked)
        self.PB_Enable_3.clicked.connect(self.slot_PB_Enable_3_clicked)
        self.PB_Polarity_1.clicked.connect(self.slot_PB_Polarity_1_clicked)
        self.PB_Polarity_2.clicked.connect(self.slot_PB_Polarity_2_clicked)
        self.PB_Polarity_3.clicked.connect(self.slot_PB_Polarity_3_clicked)
        self.LE_Volt_1.returnPressed.connect(self.slot_LE_Volt_1_returnPressed)
        self.LE_Volt_2.returnPressed.connect(self.slot_LE_Volt_2_returnPressed)
        self.LE_Volt_3.returnPressed.connect(self.slot_LE_Volt_3_returnPressed)
        self.LE_SV_1.returnPressed.connect(self.slot_LE_SV_1_returnPressed)
        self.LE_SV_2.returnPressed.connect(self.slot_LE_SV_2_returnPressed)
        self.LE_SV_3.returnPressed.connect(self.slot_LE_SV_3_returnPressed)
        self.LE_IM_1.returnPressed.connect(self.slot_LE_LE_IM_1_returnPressed)
        self.LE_IM_2.returnPressed.connect(self.slot_LE_LE_IM_2_returnPressed)
        self.LE_IM_3.returnPressed.connect(self.slot_LE_LE_IM_3_returnPressed)
        self.PB_Dir_1.clicked.connect(self.slot_PB_Dir_1_clicked)
        self.PB_Dir_2.clicked.connect(self.slot_PB_Dir_2_clicked)
        self.PB_Dir_3.clicked.connect(self.slot_PB_Dir_3_clicked)
    


    def slot_PB_Enable_1_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH1_E,True)
        else :
            self.plc.write_by_name(CH1_E,False)
    def slot_PB_Enable_2_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH2_E,True)
        else :
            self.plc.write_by_name(CH2_E,False)
    def slot_PB_Enable_3_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH3_E,True)
        else :
            self.plc.write_by_name(CH3_E,False)
        
    def slot_PB_Polarity_1_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH1_P,True)
        else :
            self.plc.write_by_name(CH1_P,False)
        self.precise_sleep(self.interval_ms[0])
        self.volt[0] = self.volt[0] +self.dir[0]*self.step_volt[0]
        self.volt[0] = 0 if self.volt[0]<0 else self.volt[0]
        self.volt[0] = 6000 if self.volt[0]>6000 else self.volt[0]
        self.plc.write_by_name(CH1_V,self.volt[0])
        self.LE_Volt_1.setText(str(self.volt[0]))
        
    def slot_PB_Polarity_2_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH2_P,True)
        else :
            self.plc.write_by_name(CH2_P,False)
        self.precise_sleep(self.interval_ms[1])
        self.volt[1] = self.volt[1] +self.dir[1]*self.step_volt[1]
        self.volt[1] = 0 if self.volt[1]<0 else self.volt[1]
        self.volt[1] = 6000 if self.volt[1]>6000 else self.volt[1]
        self.plc.write_by_name(CH2_V,self.volt[1])    
        self.LE_Volt_2.setText(str(self.volt[1]))

    def slot_PB_Polarity_3_clicked(self,checked):
        if checked:
            self.plc.write_by_name(CH3_P,True)
        else :
            self.plc.write_by_name(CH3_P,False)
        self.precise_sleep(self.interval_ms[2])
        self.volt[2] = self.volt[2] +self.dir[2]*self.step_volt[2]
        self.volt[2] = 0 if self.volt[2]<0 else self.volt[2]
        self.volt[2] = 6000 if self.volt[2]>6000 else self.volt[2]
        self.plc.write_by_name(CH3_V,self.volt[2])
        self.LE_Volt_3.setText(str(self.volt[2]))

    def slot_LE_Volt_1_returnPressed(self):
        self.volt[0] = self.LE_Volt_1.text()
        self.volt[0] = int(self.volt[0])
        self.plc.write_by_name(CH1_V,self.volt[0])
    def slot_LE_Volt_2_returnPressed(self):
        self.volt[1] = self.LE_Volt_2.text()
        self.volt[1] = int(self.volt[1])
        self.plc.write_by_name(CH2_V,self.volt[1])
    def slot_LE_Volt_3_returnPressed(self):
        self.volt[2] = self.LE_Volt_3.text()
        self.volt[2] = int(self.volt[2])
        self.plc.write_by_name(CH3_V,self.volt[2])
    def slot_LE_SV_1_returnPressed(self):
        self.step_volt[0] = self.LE_SV_1.text()
        self.step_volt[0] = int(self.step_volt[0])
    def slot_LE_SV_2_returnPressed(self):
        self.step_volt[1] = self.LE_SV_2.text()
        self.step_volt[1] = int(self.step_volt[1])
    def slot_LE_SV_3_returnPressed(self):
        self.step_volt[2] = self.LE_SV_3.text()
        self.step_volt[2] = int(self.step_volt[2])
    def slot_LE_LE_IM_1_returnPressed(self):
        self.interval_ms[0] = self.LE_IM_1.text()
        self.interval_ms[0] = int(self.interval_ms[0])
    def slot_LE_LE_IM_2_returnPressed(self):
        self.interval_ms[1] = self.LE_IM_2.text()
        self.interval_ms[1] = int(self.interval_ms[1])
    def slot_LE_LE_IM_3_returnPressed(self):
        self.interval_ms[2] = self.LE_IM_3.text()
        self.interval_ms[2] = int(self.interval_ms[2])
    def slot_PB_Dir_1_clicked(self,checked):
        self.dir[0] = 1 if checked else -1
    def slot_PB_Dir_2_clicked(self,checked):
        self.dir[1] = 1 if checked else -1
    def slot_PB_Dir_3_clicked(self,checked):
        self.dir[2] = 1 if checked else -1



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI_Twincat_Controller()
    window.show()
    sys.exit(app.exec())
