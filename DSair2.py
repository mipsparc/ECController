#coding:utf-8

import serial
import time

class DSair2:
    # 動かないぎりぎりの出力
    BASE_LEVEL = 170
    
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=115200, timeout=0.1, write_timeout=0.1, inter_byte_timeout=0.1)
        # DSair2を再起動
        self.send('reset()')
        time.sleep(1)

        # 1回目の初期化
        self.init_procedure()

        self.send('setPing()')
        init_response = self.ser.read(50)
        print(init_response)
        if (not init_response.decode('ascii').endswith('200 Ok\r\n')):
            print('DSair2を正常に認識できませんでした。終了します')
            raise ValueError('DSair2認識エラー')
        else:
            print('DSair2を正常に認識しました。')

        # 2回目の初期化
        self.init_procedure()

        print('DSair2 起動完了')

    def init_procedure(self):
        time.sleep(0.3)
        self.send('setPower(0)')
        time.sleep(0.3)
        self.send('setPower(0)')
        time.sleep(0.3)
        self.ser.reset_input_buffer()
        
    def send(self, value):
        print(value)
        self.ser.write(value.encode('ascii') + b'\n')
        self.ser.flush()

    def move_dc(self, speed_level, way):
        out_speed = int(speed_level) + self.BASE_LEVEL
        if out_speed > 1023:
            out_speed = 1023
        if out_speed < 0:
            out_speed = 0
            
        command = f'DC({out_speed},{way})\n'
        self.send(command)
    
