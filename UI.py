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
from Testcase import *
import numpy
# AMS_ID = "192.168.1.2.1.1"
# IP_ADRESS = "127.0.0.1"
# PORT = 851
CH_E = ["MAIN.Enable1","MAIN.Enable2","MAIN.Enable3"]
CH_P = ["MAIN.Polarity1","MAIN.Polarity2","MAIN.Polarity3"]
CH_V = ["MAIN.Voltage1","MAIN.Voltage2","MAIN.Voltage3"]
CH_C = ["MAIN.CurrentLimiting1","MAIN.CurrentLimiting2", "MAIN.CurrentLimiting3"]
Working_Mode = "MAIN.Working_Mode"
STATE = "MAIN.STATE"
TimeCH = ["MAIN.TimerCH[1]","MAIN.TimerCH[2]","MAIN.TimerCH[3]"]
ActiveCH = ["MAIN.ActiveCH[1]","MAIN.ActiveCH[2]","MAIN.ActiveCH[3]"]
ONCH = ["MAIN.IntervalON_CH[1]","MAIN.IntervalON_CH[2]","MAIN.IntervalON_CH[3]"]
OFFCH = ["MAIN.IntervalOFF_CH[1]","MAIN.IntervalOFF_CH[2]","MAIN.IntervalOFF_CH[3]"]

SetBool = ["MAIN.SetBool[1]","MAIN.SetBool[2]","MAIN.SetBool[3]"]
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
        self.plc.write_by_name(STATE,2)
        

        self.interval_ms = [0] * 3
        self.step_volt = [0] * 3
        self.dir = [-1] * 3
        self.volt = [0] * 3
        self.CurrentLimit = [10]* 3
        self.Test_cnt = [0]*2
        self.timers = [QTimer(self) for _ in range(3)]
        for i, timer in enumerate(self.timers):
            timer.timeout.connect(lambda i=i: self.on_timer_timeout(i))
        #page1
        self.CH_Active = np.full((2, 3), False, dtype=bool) 
        self.CH_Charge_V = np.full((2,3),0,int)
        # self.CH_Interval = np.full((2,3),0,int)
        self.CH_ON = np.full((1,3),0,int)
        self.CH_OFF = np.full((1,3),0,int)

        self.NAME_1_List=[]
        self.Enable_1_List=[]
        self.NAME_2_List = []
        self.Enable_2_List=[]
        for i in range(3):
            self.NAME_1_List.append(CH_E[i])
            self.Enable_1_List.append(False)
            self.NAME_2_List.append(CH_P[i])
            self.Enable_2_List.append(False)


        self.Polarity_2_List=[]


    def precise_sleep(self,seconds):
        start = time.perf_counter()
        while time.perf_counter() - start < seconds/1000:
            pass

    def qt_sleep(self, seconds, channel):
        self.timers[channel].start(seconds/1000)

    def on_timer_timeout(self, channel):
        self.timers[channel].stop()
        self.volt[channel] = self.volt[channel] + self.dir[channel] * self.step_volt[channel]
        self.volt[channel] = 0 if self.volt[channel] < 0 else self.volt[channel]
        self.plc.write_by_name(CH_V[channel], self.volt[channel])
        getattr(self, f'LE_Volt_{channel+1}').setText(str(self.volt[channel]))


    def setupconnect(self):
        #page0
        for i in range(3):
            getattr(self, f'PB_Enable_{i+1}').clicked.connect(lambda checked, i=i: self.slot_PB_Enable_clicked(checked, i))
            getattr(self, f'PB_Polarity_{i+1}').clicked.connect(lambda checked, i=i: self.slot_PB_Polarity_clicked(checked, i))
            getattr(self, f'PB_Dir_{i+1}').clicked.connect(lambda checked, i=i: self.slot_PB_Dir_clicked(checked, i))
            getattr(self,f'PB_VoltChange_{i+1}').clicked.connect(lambda  checked,i=i: self.slot_PB_VoltChange_clicked(checked,i))
            getattr(self, f'LE_Volt_{i+1}').returnPressed.connect(lambda i=i: self.slot_LE_Volt_returnPressed(i))
            getattr(self, f'LE_IM_{i+1}').returnPressed.connect(lambda i=i: self.slot_LE_IM_returnPressed(i))
            getattr(self, f'LE_SV_{i+1}').returnPressed.connect(lambda i=i: self.slot_LE_SV_returnPressed(i))
            getattr(self, f'LE_LC_{i+1}').returnPressed.connect(lambda i=i:self.slot_LE_LC_returnPressed(i))
        self.PB_Testcase.clicked.connect(self.slot_PB_Testcase_clicked)
        #page1
        self.PB_Exit.clicked.connect(self.slot_PB_Exit_clicked)
        for i in range(2):
            getattr(self,f'PB_Start_{i+1}').clicked.connect(lambda checked,i=i:self.slot_PB_Start_clicked(checked,i))
            getattr(self,f'PB_Syn_{i+1}').clicked.connect(lambda checked,i=i:self.slot_PB_Sync_clicked(checked,i))

            for j in range(3):
                getattr(self,f'PB_CH{j+1}_A_{i+1}').clicked.connect(lambda checked,i=i,j=j:self.slot_PB_A_clicked(checked,i,j))
                getattr(self,f'LE_CH{j+1}_CV_{i+1}').returnPressed.connect(lambda i=i,j=j:self.slot_LE_CH_CV_returnPressed(i,j))
        for z in range(3):
            getattr(self,f'LE_CH{z+1}_ON_{1}').returnPressed.connect(lambda i=z:self.slot_LE_CH_ON_returnPressed(i))
            getattr(self,f'LE_CH{z+1}_OFF_{1}').returnPressed.connect(lambda i=z:self.slot_LE_CH_OFF_returnPressed(i))

                # PB_CH1_A_1
#page0
    def slot_PB_Enable_clicked(self,checked,channel_index):
        ch_e =CH_E[channel_index]
        self.plc.write_by_name(ch_e,checked)
        

    def slot_PB_Polarity_clicked(self,checked,channel_index):
        ch_p = CH_P[channel_index]
        ch_v = CH_V[channel_index]
        self.plc.write_by_name(ch_p,checked)
        self.precise_sleep(self.interval_ms[channel_index])
        self.volt[channel_index] = self.volt[channel_index] + self.dir[channel_index] * self.step_volt[channel_index]
        self.volt[channel_index] = min(max(self.volt[channel_index], 0), 6000)
        self.plc.write_by_name(ch_v,self.volt[channel_index])
        getattr(self,f'LE_Volt_{channel_index+1}').setText(str(self.volt[channel_index]))


    def slot_PB_Dir_clicked(self,checked,channel_index):
        self.dir[channel_index] = 1 if checked else -1
        # self.thread_1 = Testcase_1(self)
        # self.thread_1.start()

    def slot_PB_VoltChange_clicked(self,checked,channel_index):
        self.volt[channel_index] = self.volt[channel_index] + self.dir[channel_index] * self.step_volt[channel_index]
        self.volt[channel_index] = min(max(self.volt[channel_index], 0), 6000)
        self.plc.write_by_name(CH_V[channel_index],self.volt[channel_index])
        getattr(self,f'LE_Volt_{channel_index+1}').setText(str(self.volt[channel_index]))


    def slot_LE_LC_returnPressed(self,channel_index):
        ch_c = CH_C[channel_index]
        self.CurrentLimit[channel_index]= getattr(self,f'LE_LC_{channel_index+1}').text()
        self.CurrentLimit[channel_index] = int(self.CurrentLimit[channel_index])
        self.plc.write_by_name(ch_c,self.CurrentLimit[channel_index])
        

    def slot_LE_Volt_returnPressed(self,channel_index):
        ch_v = CH_V[channel_index]
        self.volt[channel_index] = getattr(self,f'LE_Volt_{channel_index+1}').text()
        self.volt[channel_index] = int(self.volt[channel_index])
        self.volt[channel_index] = min(max(0,self.volt[channel_index]),6000)
        self.plc.write_by_name(ch_v,self.volt[channel_index])
        getattr(self,f'LE_Volt_{channel_index+1}').setText(str(self.volt[channel_index]))



    def slot_LE_IM_returnPressed(self,channel_index):
        self.interval_ms[channel_index] = getattr(self,f'LE_IM_{channel_index+1}').text()
        self.interval_ms[channel_index] = int(self.interval_ms[channel_index])


    def slot_LE_SV_returnPressed(self,channel_index):
        self.step_volt[channel_index] = getattr(self,f'LE_SV_{channel_index+1}').text()
        self.step_volt[channel_index] = int(self.step_volt[channel_index])
        
    def slot_PB_Testcase_clicked(self):
        self.stackedWidget.setCurrentIndex(1)  
        self.plc.write_by_name(Working_Mode,0)



#page1 
    def slot_PB_Exit_clicked(self,checked):
        self.stackedWidget.setCurrentIndex(0)
        self.plc.write_by_name(STATE,2)
        self.plc.write_by_name(Working_Mode,0)


    def slot_PB_A_clicked(self,checked,test_index,channel_index):
        self.CH_Active[test_index][channel_index] = checked
        print(test_index,channel_index, self.CH_Active[test_index][channel_index])
        if CH_E[channel_index] in getattr(self,f'NAME_{test_index+1}_List'):
            index = getattr(self,f'NAME_{test_index+1}_List').index(CH_E[channel_index])
            getattr(self,f'Enable_{test_index+1}_List')[channel_index] = checked
        else:
            getattr(self,f'Enable_{test_index+1}_List').append(checked)
            getattr(self,f'NAME_{test_index+1}_List').append(CH_E[channel_index])
        print(getattr(self,f'NAME_{test_index+1}_List'),getattr(self,f'Enable_{test_index+1}_List'))
        self.plc.write_by_name(ActiveCH[channel_index],checked)
        self.PB_Syn_1.setChecked(False)
        self.PB_Syn_2.setChecked(False)



    def slot_LE_CH_CV_returnPressed(self,test_index,channel_index):
        self.CH_Charge_V[test_index][channel_index] =  getattr(self,f'LE_CH{channel_index+1}_CV_{test_index+1}').text()
        self.CH_Charge_V[test_index][channel_index] = int(self.CH_Charge_V[test_index][channel_index])
        print(test_index,channel_index,self.CH_Charge_V[test_index][channel_index])    
        ch_v = CH_V[channel_index]
        self.plc.write_by_name(ch_v,self.CH_Charge_V[test_index][channel_index])
        self.PB_Syn_1.setChecked(False)
        self.PB_Syn_2.setChecked(False)


    def slot_LE_CH_ON_returnPressed(self,test_index,channel_index):
        self.CH_ON[test_index][channel_index] = getattr(self,f'LE_CH{channel_index+1}_ON_{test_index+1}').text()
        self.CH_ON[test_index][channel_index] = int(self.CH_ON[test_index][channel_index])
        self.CH_ON[test_index][channel_index] =self.CH_ON[test_index][channel_index]/10
        print(test_index,channel_index,self.CH_ON[test_index][channel_index])
        self.plc.write_by_name(ONCH[channel_index],self.CH_ON[test_index][channel_index])
        self.PB_Syn_1.setChecked(False)
        self.PB_Syn_2.setChecked(False)
    
    def slot_LE_CH_OFF_returnPressed(self,test_index,channel_index):
        self.CH_OFF[test_index][channel_index] = getattr(self,f'LE_CH{channel_index+1}_OFF_{test_index+1}').text()
        self.CH_OFF[test_index][channel_index] = int(self.CH_OFF[test_index][channel_index])
        self.CH_OFF[test_index][channel_index] =self.CH_OFF[test_index][channel_index]/10
        print(test_index,channel_index,self.CH_OFF[test_index][channel_index])
        self.plc.write_by_name(OFFCH[channel_index],self.CH_OFF[test_index][channel_index])
        self.PB_Syn_1.setChecked(False)
        self.PB_Syn_2.setChecked(False)

    def slot_PB_Start_clicked(self,checked,test_index):
        if checked:
            if(test_index == 0):
                self.plc.write_by_name(Working_Mode,1)
                self.plc.write_by_name(STATE,3)
                self.PB_Start_2.setChecked(False)
                
                # self.PB_Start_2.setChecked(False)
                # self.Thread_1 = Testcase_1(self)
                # self.Thread_1.plc_write_by_name_signal.connect(self.plc.write_by_name)
                # self.Thread_1.start()
            elif (test_index == 1):
                self.plc.write_by_name(STATE,3)
                self.plc.write_by_name(Working_Mode,2)
                self.PB_Start_1.setChecked(False)

                # self.PB_Start_1.setChecked(False)
                # self.thread_2 = Testcase_2(self)
                # self.Thread_1.plc_write_by_name_signal.connect(self.plc.write_by_name)
                # self.thread_2.start()
        else :
            self.plc.write_by_name(STATE,2)
            self.plc.write_by_name(Working_Mode,0)
            for i in range(3):
                self.plc.write_by_name(TimeCH[i],0)
                self.plc.write_by_name(CH_E[i],False)
                self.plc.write_by_name(SetBool[i],False)


    def slot_PB_Sync_clicked(self,checked,test_index):
        self.PB_Syn_1.setChecked(checked)
        self.PB_Syn_2.setChecked(checked)
        if(checked):
            self.CH_ON[0][1] = self.CH_ON[0][2] = self.CH_ON[0][0]
            self.CH_OFF[0][1] = self.CH_OFF[0][2] = self.CH_OFF[0][0]
            self.CH_Charge_V[0][1] = self.CH_Charge_V[0][2] = self.CH_Charge_V[0][0]
            self.CH_Active[0][1] = self.CH_Active[0][2] = self.CH_Active[0][0] 
            for _ in range(3):
                self.plc.write_by_name(ONCH[_],self.CH_ON[0][_])
                self.plc.write_by_name(OFFCH[_],self.CH_OFF[0][_])
                self.plc.write_by_name(CH_V[_],self.CH_Charge_V[0][_])
                self.plc.write_by_name(SetBool[_],self.CH_Charge_V[0][_])
                self.plc.write_by_name(ActiveCH[_],self.CH_Active[0][_])
                getattr(self,f'PB_CH{_+1}_A_1').setChecked(self.CH_Active[0][_])
                getattr(self,f'LE_CH{_+1}_CV_1').setText(str(self.CH_Charge_V[0][_]))
                getattr(self,f'LE_CH{_+1}_ON_1').setText(str(self.CH_ON[0][_]*10))
                getattr(self,f'LE_CH{_+1}_OFF_1').setText(str(self.CH_OFF[0][_]*10))



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = UI_Twincat_Controller()
    window.show()
    sys.exit(app.exec())
