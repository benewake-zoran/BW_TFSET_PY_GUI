import time

# 防止IIC转接板卡死
def refresh_IIC(self):
    if self.ser.rts is False:  # IIC转接板卡死复位
        self.ser.setRTS(True)
        self.ser.setRTS(False)
        rx = self.ser.read(2)
        if rx != b'':
            print(rx.hex())

