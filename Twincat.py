import pyads
from ctypes import sizeof
AMS_ID = "192.168.1.2.1.1"
IP_ADRESS = "127.0.0.1"
PORT = 851
import time
plc = pyads.Connection(AMS_ID,PORT,IP_ADRESS)
try :
    plc.open()
    bool_value = False
    
    plc.write_by_name("MAIN.Voltage3",1000)
    for i in range(100):
        # plc.write_by_name('MAIN.Enable3', True, pyads.PLCTYPE_BOOL)
        plc.write_by_name('MAIN.Polarity3', True, pyads.PLCTYPE_BOOL)
        # plc.write_by_name('MAIN.Enable3',False, pyads.PLCTYPE_BOOL)

        time.sleep(0.5)
        val_read_back = plc.read_by_name('MAIN.Enable3', pyads.PLCTYPE_BOOL)
        print(f"读取到的 MAIN.Enable1 值为: {val_read_back}")
        # plc.write_by_name('MAIN.Enable3', False, pyads.PLCTYPE_BOOL)
        plc.write_by_name('MAIN.Polarity3', False, pyads.PLCTYPE_BOOL)
        # plc.write_by_name('MAIN.Enable3',False, pyads.PLCTYPE_BOOL)

        time.sleep(0.5)
        # print(f"已经将 MAIN.Enable1 置为: {bool_value}")
        val_read_back = plc.read_by_name('MAIN.Enable3', pyads.PLCTYPE_BOOL)
        print(f"读取到的 MAIN.Enable1 值为: {val_read_back}")

finally:
    plc.close()
