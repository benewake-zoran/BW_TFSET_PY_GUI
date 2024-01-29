import time
import serial
import crcmod

DIS_CMD = 'ADDR 03 00 00 00 01'  # 测距指令
DIS_DIFF = 6  # 允许测距误差范围 
FPS_DIFF = 20  # 允许帧率误差范围
RECV_FRAME_HEADER = b'YY'  # 接收数据帧头定义 0x59 0x59


# 定义Modbus CRC16校验码生成函数
def ModbusCRC16(data):
    crc16 = crcmod.predefined.Crc('modbus')  # 创建一个CRC校验对象
    crc16.update(data)  # 添加指令
    crc = crc16.crcValue.to_bytes(2, byteorder='little')
    return crc


# 判断测距回显是否正确
def checkDataFrame_MODBUS(self):
    time.sleep(0.03)
    if self.ser.in_waiting:
        rx = self.ser.read(7)
        if rx[1] == 0x03 and rx[2] == 0x02:
            self.rx = rx
            print('rx:', rx.hex())
            return True
    return False


# 轮询从机地址
def pollID_MODBUS(self):  
    start_time = time.time()
    for id in range(1, 248):
        SlaveID = hex(id)[2:].zfill(2).upper()  # 将十进制转十六进制
        modCmd_str = DIS_CMD.replace('ADDR', SlaveID)  # 更新测距指令
        modCmd = bytes.fromhex(modCmd_str)
        crc = ModbusCRC16(modCmd)  # 计算校验码
        modCmd += crc
        print('id:', id, 'modCmd:', ' '.join(format(x, '02X') for x in modCmd))
        self.ser.reset_input_buffer()
        self.ser.write(modCmd)
        if checkDataFrame_MODBUS(self):
            self.SlaveID = '0x{:02X}'.format(modCmd[0], byteorder='big')  #十六进制bytes转固定两位的十六进制str  如(bytes)  0A ->  (str) 0x0A
            self.MODBUSCmd = modCmd
            
            print('check finish, modCmd[0]:', modCmd[0])
            print('check finish, self.SlaveID:', self.SlaveID)
            print('self.MODBUSCmd:', self.MODBUSCmd.hex(), 'self.rx:', self.rx.hex())
            self.newCmd = modCmd #保存数据，用来生成TXT文本信息
            print('self.newCmd ',self.newCmd )
            diff = time.time() - start_time
            print('diff:', diff)
            print('------------------------------')
            return self.SlaveID
    self.newCmd = modCmd #保存数据，用来生成TXT文本信息
    self.rx = b''
    self.MODBUSCmd = b''
    diff = time.time() - start_time
    print('diff:', diff)
    print('------------------------------')
    return None


# 若 JSON 文件有指令发送,则根据从机地址改写并发送指令
def sendCmd_MODBUS(self):
    
            print('common cmd:', self.data[self.index]['cmd'])  # 获取对应的指令
        #if self.data[self.index]['cmd'] != '':  # 判断指令是否为空
            # SlaveID 为空，轮询波特率和地址   
            if self.SlaveID is None:
                pollID_MODBUS(self)

            if self.SlaveID is not None:
               if self.data[self.index]['widget'] == 'QLabel':       
                    Cmd_str = self.data[self.index]['cmd'].replace('ADDR', self.SlaveID[2:])
                    print('1 Cmd_str:', Cmd_str)
                    Cmd = bytes.fromhex(Cmd_str)  # str 转为 byte
                    crc = ModbusCRC16(Cmd)  # 计算校验和
                    Cmd += crc  # 加上校验和后的指令
                    print('2 Cmd_byte:', Cmd)
                    self.newCmd = Cmd
                    print('self.MODBUSCmd_hex:', self.newCmd.hex())
                    self.ser.reset_input_buffer()
                    self.ser.write(self.newCmd)
                    print('------------------------------')
               elif self.data[self.index]['widget'] == 'QLineEdit':
                     self.editVal = self.widgetslist[self.index].text() # 获取文本框输入值  
                     print('editVal:', self.editVal)
                     lineEditCmd_Modbus(self)
                     self.ser.reset_input_buffer()
                     print(self.newCmd)
                     self.ser.write(self.newCmd)
               elif self.data[self.index]['widget'] == 'QComboBox':
                    self.boxVal = self.widgetslist[self.index].currentText()  # 获取当前下拉列表值  根据这个 选项 序号
                    print('boxVal:', self.boxVal)
                    comboBoxCmd(self)
                    self.ser.reset_input_buffer()
                    self.ser.write(self.newCmd)
                    if self.newCmd1 != '':
                        time.sleep(0.5)
                        self.ser.write(self.newCmd1)
                    

# 发送指令后接收指令回显并判断
def recvData_MODBUS(self):
    start_time = time.time()
    while True:
        if self.ser.in_waiting:
            rxhead = self.ser.read(1)  # 读取头字节
            rxfuncode = self.ser.read(1)  # 读取功能码
            print('rxhead:', rxhead.hex(), 'rxfuncode:', rxfuncode.hex())
            if rxfuncode[0] == 0x03:  # 判断回显 SlaveID 是否和发送的相同
                if rxhead == bytes.fromhex(self.SlaveID[2:]):
                    rxlen = self.ser.read(1)  # 读取一个长度字节
                    rxlenint = rxlen[0]  # 将bytes转为int
                    rxdata = self.ser.read(rxlenint + 2)  # 读取剩下的数据字节加CRC
                    self.rx = rxhead + rxfuncode + rxlen + rxdata
                    print('rx==head self.rx:', self.rx.hex())
                    break
            else:  #0x06 
                print('rx head is not SlaveID')  # 帧头不是 SlaveID 接收剩下数据观察
                if self.data[self.index]['name'] == '波特率':
                    rxdata = self.ser.read(6+8) #波特率收了两次消息，因此多读8位
                else :
                    rxdata = self.ser.read(6)  #H：只接收8位，就不会在关闭Modbus保存之后卡死
                self.rx = rxhead + rxfuncode + rxdata
                print('rx!=head self.rx:', self.rx.hex())
                break

        elif (time.time() - start_time) > 3:  # 超过 3s 都无数据接收
            #pollID_MODBUS(self)  # 尝试再次轮询地址,看是否是发送指令的读写地址位错误
            sendCmd_MODBUS(self)  # 轮询地址后再次尝试发送指令
            time.sleep(0.1)
            if self.ser. in_waiting:
                rxhead = self.ser.read(1)
                rxfuncode = self.ser.read(1)
                # rxdata = self.ser.readall()
                if rxhead == bytes.fromhex(self.SlaveID[2:]) and rxfuncode[0] == 0x03:
                    rxlen = self.ser.read(1)
                    rxlenint = rxlen[0]
                    rxdata = self.ser.read(rxlenint + 2)
                    self.rx = rxhead + rxfuncode + rxlen + rxdata
                    print('time out retry self.rx:', self.rx.hex())
                    break
                else:
                    rxdata = self.ser.read(20)
                    self.rx = rxhead + rxfuncode + rxdata
                    print('time out retry rxhead is not SlaveID')
                    print('time out retry self.rx:', self.rx.hex())
                    break
            else:
                print('time out retry no rx')
                self.rx = b''
                self.widgetslist[self.index].setText('')
            break
    print('------------------------------')

#函数名：nameType_Modbus(self)
#功能：根据标签判断回显
def nameType_Modbus(self):
    #第一种：读取后计算并显示
    if self.data[self.index]['name'] == '固件版本' or self.data[self.index]['name'] == 'FirmwareVer':
        if self.rx != b'' and self.rx[1] == 0x03 and self.rx[2] == 0x04:
            version_rxhex = self.rx[4:7].hex()
            # 每两个字符由hex转为int，用'.'连接为str
            version_rxstr = '.'.join(str(int(version_rxhex[i:i + 2], 16)) for i in range(0, len(version_rxhex), 2))
            self.widgetslist[self.index].setText(version_rxstr)
            recvJudge_MODBUS(self)
            print('固件版本是：', version_rxstr)
            print('------------------------------')
        recvJudge_MODBUS(self)
    elif self.data[self.index]['name'] == '测距结果' or self.data[self.index]['name'] == 'RangingResult':
        if self.rx != b'' and self.rx[1] == 0x03 and self.rx[2] == 0x02:
            self.dist = int.from_bytes(self.rx[3:5], byteorder='big')
            self.widgetslist[self.index].setText(str(self.dist) + ' (cm)')
            print('测距结果是：', self.dist)
            print('------------------------------')
        recvJudge_MODBUS(self)
    elif self.data[self.index]['name'] == '测试强度' or self.data[self.index]['name'] == 'TestStrength':
        if self.rx != b'' and self.rx[1] == 0x03 and self.rx[2] == 0x02:
            strength = int.from_bytes(self.rx[3:5], byteorder='big')
            self.widgetslist[self.index].setText(str(strength))
            print('测试强度是：', strength)
            print('------------------------------')
        recvJudge_MODBUS(self)
    
    #第二种，发出不一样的指令，回传是一样的指令，例：设置帧率      
    elif (self.data[self.index]['name'] == '输出帧率' or self.data[self.index]['name'] == '低功耗模式' or self.data[self.index]['name'] == '保存配置' or 
            self.data[self.index]['name'] == '重启' or self.data[self.index]['name'] == 'Modbus协议关闭' or self.data[self.index]['name'] == '设置SlaveID' or 
            self.data[self.index]['name'] == '恢复出厂设置' or self.data[self.index]['name'] == '工作模式' or self.data[self.index]['name'] == '波特率' ):
        if self.rx[0:8] != self.newCmd: #回显和发送不一致
            print('self.rx',self.rx[0:8])
            print('self.newCmd',self.newCmd)
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
        else:                      #回显和发送一致
            if(self.data[self.index]['name'] == '保存配置' or self.data[self.index]['name'] == '重启'  ):
               self.clearLabel()   #成功保存或者重启后清除其他标签的提示
            self.labelReturnlist[self.index].setText('OK')  
            self.labelReturnlist[self.index].setStyleSheet('color: green')
            
    #第三种，发出指令后回传不一样

# 判断期望值和检查值是否相同(方法同UART)
def recvJudge_MODBUS(self):
    if self.data[self.index]['widget'] == 'QLabel' or self.data[self.index]['widget'] == 'QLineEdit':
        if  self.widgetslist[self.index].text() != ''  and self.rx != b'':
            self.labelReturnlist[self.index].setText('OK')
            self.labelReturnlist[self.index].setStyleSheet('color: green') 
        else :
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')
    elif self.data[self.index]['widget'] == 'QComboBox':
        if self.widgetslist[self.index].currentText() != '':
            self.labelReturnlist[self.index].setText('OK')
            self.labelReturnlist[self.index].setStyleSheet('color: green')
        else:
            self.labelReturnlist[self.index].setText('NG')
            self.labelReturnlist[self.index].setStyleSheet('color: red')


# 通过轮询检查 Slave ID
def checkSlaveID_MODBUS(self):
    pollID_MODBUS(self)  # 轮询波特率和地址
    if self.SlaveID is not None and self.rx != b'':
        self.widgetslist[self.index].setText('HEX:'+self.SlaveID+' DEC:'+str(int(self.SlaveID, 16)))
    else:
        self.widgetslist[self.index].setText('')
    if self.widgetslist[self.index].text() != '':
            self.labelReturnlist[self.index].setText('OK')
            self.labelReturnlist[self.index].setStyleSheet('color: green')
    else :
        self.labelReturnlist[self.index].setText('NG')
        self.labelReturnlist[self.index].setStyleSheet('color: red') 


# 检查输出帧率
def checkFramerate_MODBUS(self):
    # 计算帧率
    self.ser.reset_input_buffer()
    start_time = time.time()
    frame_count = 0
    while True:
        rx = self.ser.read(9)
        if len(rx) == 9:
            frame_count += 1
        endtime = time.time()
        time_diff = endtime - start_time
        if time_diff >= 1:
            fps = frame_count / time_diff  # 计算帧率
            print('Frame rate: {:.2f} Hz'.format(fps))
            break
    self.widgetslist[self.index].setText(str(round(fps)) + ' (Hz)')
    # 判断帧率是否正确
    if self.data[self.index]['std'] != '':
        stdfps = int(self.data[self.index]['std'])
    else:
        stdfps = 0
    # 判断结果是 OK 还是 NG
    if self.data[self.index]['std'] == '' and self.widgetslist[self.index].text() != '':
        self.labelReturnlist[self.index].setText('OK')
        self.labelReturnlist[self.index].setStyleSheet('color: green')
        print('Framerate is Correct')
    elif self.data[self.index]['std'] != '' and abs(fps - stdfps) <= FPS_DIFF:
        self.labelReturnlist[self.index].setText('OK')
        self.labelReturnlist[self.index].setStyleSheet('color: green')
        print('Framerate is Correct')
    else:
        self.labelReturnlist[self.index].setText('NG')
        self.labelReturnlist[self.index].setStyleSheet('color: red')
        print('Framerate is Error')

    self.rx = b''
    self.MODBUSCmd = b''
    print('------------------------------')


def checkOther_MODBUS(self):
    self.SlaveID = pollID_MODBUS(self)
    if self.SlaveID is not None:
        dist = int.from_bytes(self.rx[3:5], byteorder='big')
        text = 'ID:' + self.SlaveID + ' D:' + str(dist) + 'cm'
        self.widgetslist[self.index].setText(text)

    recvJudge_MODBUS(self)

#函数名:lineEditCmd_Modbus(self)
#功能:处理文本输入框内容，合成指令
def lineEditCmd_Modbus(self):
    priCmd = self.data[self.index]['cmd'].replace('ADDR', self.SlaveID[2:]) 
    print(self.SlaveID)
    print('priCmd:', priCmd)
    priCmdhex_list = priCmd.split()  # 字符串存进一个列表
    priCmdhead_str = priCmdhex_list[0]  # Slave ID
    priCmdFunc_str = priCmdhex_list[1]  # 读/写 功能码
    priCmdidH_str = priCmdhex_list[2]  # 寄存器地址H
    priCmdidL_str = priCmdhex_list[3]  # 寄存器地址L
    priCmddataH_list = priCmdhex_list[4]  # 寄存器写入的数据H
    priCmddataL_list = priCmdhex_list[5]  # 寄存器写入的数据L
    print('priCmddata_list:', priCmddataH_list,priCmddataL_list)


    if self.data[self.index]['name'] == '输出帧率':  
        outframeVal_hexstr = hex(int(self.editVal))  # 将输入值转为十六进值字符串
        outframeVal_str = outframeVal_hexstr[2:]  # 将十六进制中的0x字符去掉
        outframeVal_str0 = outframeVal_str.rjust(4, '0')  # 补齐到4位不足添0
        outframeVal_list = [outframeVal_str0[i:i + 2] for i in range(0, len(outframeVal_str0), 2)]  # 每两个字符分割并存进列表
        print('outframeVal_list:', outframeVal_list)
        priCmddataL_list = outframeVal_list[1] # 将输入低字节填入 LL 字符串
        priCmddataH_list = outframeVal_list[0] # 将输入高字节填入 HH 字符串
        print('outframeVal_list:', priCmddataH_list,priCmddataL_list)
    
    if self.data[self.index]['name'] == '低功耗模式':  
        outframeVal_hexstr = hex(int(self.editVal))  # 将输入值转为十六进值字符串
        outframeVal_str = outframeVal_hexstr[2:]  # 将十六进制中的0x字符去掉
        outframeVal_str0 = outframeVal_str.rjust(4, '0')  # 补齐到4位不足添0
        outframeVal_list = [outframeVal_str0[i:i + 2] for i in range(0, len(outframeVal_str0), 2)]  # 每两个字符分割并存进列表
        print('outframeVal_list:', outframeVal_list)
        priCmddataL_list = outframeVal_list[1] # 将输入低字节填入 LL 字符串
        priCmddataH_list = outframeVal_list[0] # 将输入高字节填入 HH 字符串
        print('outframeVal_list:', priCmddataH_list,priCmddataL_list)

    elif  self.data[self.index]['name'] == '设置SlaveID':  
        outframeVal_hexstr = hex(int(self.editVal))  # 将输入值转为十六进值字符串
        outframeVal_str = outframeVal_hexstr[2:]  # 将十六进制中的0x字符去掉
        outframeVal_str0 = outframeVal_str.rjust(4, '0')  # 补齐到4位不足添0
        outframeVal_list = [outframeVal_str0[i:i + 2] for i in range(0, len(outframeVal_str0), 2)]  # 每两个字符分割并存进列表
        print('outframeVal_list:', outframeVal_list)
        priCmddataL_list = outframeVal_list[1] # 将输入低字节填入 LL 字符串
        priCmddataH_list = outframeVal_list[0] # 将输入高字节填入 HH 字符串
        print('outframeVal_list:', priCmddataH_list,priCmddataL_list)
      

    newCmdstr = priCmdhead_str + priCmdFunc_str + priCmdidH_str +  priCmdidL_str + priCmddataH_list + priCmddataL_list 
    print(newCmdstr)
    self.newCmd = bytes.fromhex(newCmdstr)  # str 转为 byte
    crc = ModbusCRC16(self.newCmd)  # 计算校验和
    self.newCmd += crc  # 加上校验和后的指令
    print(self.newCmd)


#函数名：comboBoxCmd(self)
#功能：根据下拉选项的序号，指定发送的指令
def comboBoxCmd(self):
    priCmd_list = self.data[self.index]['cmd']
    index = self.widgetslist[self.index].currentIndex()
    print('priCmd_list:', priCmd_list)
    if self.data[self.index]['name'] == '波特率':
        baudCmd_list = [    
                            [#波特率高字节
                             'ADDR 06 00 83 00 00', 'ADDR 06 00 83 00 00', 'ADDR 06 00 83 00 00', 'ADDR 06 00 83 00 00',
                             'ADDR 06 00 83 00 01', 'ADDR 06 00 83 00 03', 'ADDR 06 00 83 00 07', 'ADDR 06 00 83 00 0E'
                            ],
                            [#波特率低字节
                             'ADDR 06 00 84 25 80', 'ADDR 06 00 84 4B 00', 'ADDR 06 00 84 96 00', 'ADDR 06 00 84 E1 00',
                             'ADDR 06 00 84 C2 00', 'ADDR 06 00 84 E8 00', 'ADDR 06 00 84 08 00', 'ADDR 06 00 84 10 00'                          
                            ]
                       ]
        comboboxCmd  = baudCmd_list[0][index]
        comboboxCmd1 = baudCmd_list[1][index]
    else:
        comboboxCmd = priCmd_list[index]
        comboboxCmd1 = ''
    print(self.SlaveID)
    self.newCmd  =  bytes.fromhex(comboboxCmd.replace('ADDR', self.SlaveID[2:]) )
    crc = ModbusCRC16(self.newCmd)  # 计算校验和
    self.newCmd += crc  # 加上校验和后的指令
    print(self.newCmd)
    if comboboxCmd1 != '':
       self.newCmd1 = bytes.fromhex(comboboxCmd1.replace('ADDR', self.SlaveID[2:]) )
       crc = ModbusCRC16(self.newCmd1)  # 计算校验和
       self.newCmd1 += crc  # 加上校验和后的指令
       print(self.newCmd1)
    else: 
       self.newCmd1 = ''

    print('index:', index, 'comboboxCmd:', comboboxCmd, 'newCmdbytes:', self.newCmd)
    print('index:', index, 'comboboxCmd1:', comboboxCmd1, 'newCmdbytes1:', self.newCmd1)
    
    print('------------------------------')
