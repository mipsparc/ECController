#coding: utf-8
import time
import OHC_PC01A
import DSair2
import Sound

# 電車鉄道模型をリアルに運転するシステム
# サンイン重工 OHC-PC01Aコントローラ、DesktopStation DSair2が必要

# DSair2のシリアルポート。Linuxでほかに機器がなければこのまま
dsair2_port = '/dev/ttyUSB0'

#DSair2初期化
dsair2 = DSair2.DSair2(dsair2_port)

# 主幹制御器読み込み初期化
mascon = OHC_PC01A.OHC_PC01A()

# 音
sounds = Sound.Sound()

# メインループを0.1秒おきに回すためのunix timeカウンタ
last_counter = time.time()

speed_level = 0

while True:
    try:
        # 主幹制御器
        mascon.loadStatus()
        
        # ミュージックホーン
        sounds.horn(mascon.white)
        
        #仮実装 あとで実車にもとづいた加速度にする
        speed_level += mascon.accel_knotch * 2
        speed_level -= mascon.brake_knotch * 2
        if speed_level < 0:
            speed_level = 0
        if speed_level > 600:
            speed_level = 600
        
        dsair2.move_dc(speed_level, mascon.way)
        
        # 0.1秒経過するまで待つ(sleepしないのは、音などの影響を回避するため)
        while (time.time() <= last_counter + 0.1):
            pass
        last_counter = time.time()
    
    except:
        # 異常終了・正常終了時に走行などが停止する
        # 念の為3回送出する
        dsair2.move_dc(0, 1)
        dsair2.move_dc(0, 1)
        dsair2.move_dc(0, 1)
        # 伝搬するまで待つ
        time.sleep(0.5)
        
        raise
