#coding: utf-8
import time
import OHC_PC01A
import DSair2
import Sound
import EC

# 電車鉄道模型をリアルに運転するシステム
# サンイン重工 OHC-PC01Aコントローラ、DesktopStation DSair2が必要

# DSair2のシリアルポート。Linuxでほかに機器がなければこのまま
dsair2_port = '/dev/ttyUSB0'

#DSair2初期化
dsair2 = DSair2.DSair2(dsair2_port)

# 主幹制御器読み込み初期化
mascon = OHC_PC01A.OHC_PC01A()

# 音初期化
sound = Sound.Sound()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

speed_level = 0
ec = EC.EC('e531')
dsair2.turnOnLight()

while True:
    try:
        # 主幹制御器
        mascon.loadStatus()
        
        # ドア
        sound.door(mascon.zero)
        
        # ミュージックホーン
        sound.music_horn(mascon.yellow)
        
        # 通常ホーン
        sound.horn(mascon.three)
        
        # 徐行
        sound.slow_start(mascon.five)

        # チンベル
        sound.ding_bell(mascon.four)
        
        speed_level = ec.calcSpeed(speed_level, mascon.accel_knotch, mascon.brake_knotch)
        
        dsair2.move(speed_level, mascon.way)
        
        if mascon.way == 0:
            dsair2.turnOffLight()
        else:
            dsair2.turnOnLight()
        
        # 0.1秒経過するまで待つ
        while (time.time() <= last_counter + 0.1):
            time.sleep(0.001)
        last_counter = time.time()
    
    except:
        # 異常終了・正常終了時に走行などが停止する
        dsair2.move(0, 1)
        # 伝搬するまで待つ
        time.sleep(0.5)
        
        raise

