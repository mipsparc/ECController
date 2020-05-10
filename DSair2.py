#coding:utf-8

# DesktopStation DSair2への接続ライブラリ

import serial
import time

class DSair2:
    # 動かないぎりぎりの出力
    BASE_LEVEL = 170
    
    # デコーダアドレスは現状固定
    LOCO_ADDR = 3
    
    def __init__(self, port):
        self.ser = serial.Serial(port, baudrate=115200, timeout=0.1, write_timeout=0.1, inter_byte_timeout=0.1)
        # DSair2を再起動
        self.send('reset()')
        time.sleep(1)

        self.ser.reset_input_buffer()
        self.send('setPing()')
        init_response = self.ser.read(50)
        print(init_response)
        if (not init_response.decode('ascii').endswith('200 Ok\r\n')):
            print('DSair2を正常に認識できませんでした。終了します')
            raise ValueError('DSair2認識エラー')
        else:
            print('DSair2を正常に認識しました。')

        # DCC初期化
        self.send('setPower(1)')
        poweron_response = self.ser.read(50)
        print(poweron_response)
        time.sleep(0.5)
        self.ser.reset_input_buffer()

        print('DSair2 起動完了')
        
        self.last_out_speed = 0
        self.last_way = 0

    def send(self, value):
        print(value)
        self.ser.write(value.encode('ascii') + b'\n')
        self.ser.flush()
        
    def move(self, speed_level, way):
        self.move_dcc(speed_level, way)
        
    # 速度や方向などの状態が変わるときのみ命令を出力する
    def move_dcc(self, speed_level, way):
        out_speed = int(speed_level) + self.BASE_LEVEL
        if out_speed > 1023:
            out_speed = 1023
        if out_speed < 0:
            out_speed = 0
        # 仮想的な方向 0(切)
        if way == 0:
            out_speed = 0
        
        if out_speed != self.last_out_speed:
            self.last_out_speed = out_speed
            self.send(f'setLocoSpeed({self.LOCO_ADDR},{out_speed},2)')
        
        if way != self.last_way:
            self.last_way = way
            # 仮想的な方向 0(切) は送信しない
            if way != 0:
                self.send(f'setLocoDirection({self.LOCO_ADDR},{way})')
    
    # 現在は使用していないが、参考用にとっておく。DC駆動用
    def move_dc(self, speed_level, way):
        out_speed = int(speed_level) + self.BASE_LEVEL
        if out_speed > 1023:
            out_speed = 1023
        if out_speed < 0:
            out_speed = 0
            
        command = f'DC({out_speed},{way})\n'
        self.send(command)
    
    # 現在は使用していないが、参考用にとっておく。DC駆動時の初期化用
    def init_procedure_for_dc(self):
        time.sleep(0.3)
        self.send('setPower(0)')
        time.sleep(0.3)
        self.send('setPower(0)')
        time.sleep(0.3)
        self.ser.reset_input_buffer()
    
