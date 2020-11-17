#coding: utf-8
import time
import OHC_PC01A
import DSair2
import Sound
import EC
from sys import argv

# 電車鉄道模型をリアルに運転するシステム
# サンイン重工 OHC-PC01Aコントローラ、DesktopStation DSair2が必要

# DSair2のシリアルポート。Linuxでほかに機器がなければこのまま
dsair2_port = '/dev/ttyUSB0'

# 主幹制御器読み込み初期化
mascon = OHC_PC01A.OHC_PC01A()

# 音初期化
sound = Sound.Sound()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

# 車種選択
if len(argv) != 1:
    car = argv[1]
else:
    print('\n-----------------------\n')
    print('車種を選んでください\n')
    for car, data in EC.EC.CARS.items():
        print('車種ID {}: {}'.format(car, data['desc']))
    car = input('\n車種IDを入力> ')

ec = EC.EC(car)

#DSair2初期化
dsair2 = DSair2.DSair2(dsair2_port, ec.isDcc())

print('\n-----------------------\n')
print('初期化完了\n')

while True:
    try:
        # 主幹制御器
        mascon.loadStatus()
        
        # ドア
        sound.door(mascon.zero)
        
        # ミュージックホーン
        sound.music_horn(mascon.yellow)
        
        # 通常ホーン
        sound.horn(mascon.five)
        
        # 徐行
        sound.slow_start(mascon.four)

        # チンベル
        sound.ding_bell(mascon.three)
        
        # 非常ブレーキ緩解
        sound.air_out(mascon.brake_knotch)
        
        # 次は停車
        sound.stop(mascon.white)
        
        speed_level = ec.calcSpeed(mascon.accel_knotch, mascon.brake_knotch)
                
        dsair2.move(speed_level, mascon.way)
        
        # 0.1秒経過するまで待つ
        while (time.time() <= last_counter + 0.1):
            time.sleep(0.001)
        last_counter = time.time()
    
    except:
        # 異常終了・正常終了時に走行などが停止する
        dsair2.move(0, 0)
        # 伝搬するまで待つ
        time.sleep(0.5)
        
        raise

