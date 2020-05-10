# 概要
このソフトウェア群は、ワンハンドルマスコンと鉄道模型コントローラで鉄道模型をリアルに制御するシミュレータシステムです。

# やりたいこと
- 電車のモデルオブジェクト作成して実車に近い加減速
- 音

# 最初の手順
1. dialoutグループにユーザーを入れる `sudo adduser $USER dialout`
1. udev設定をする `sudo cp udev_rules/99-dsair2.rules /etc/udev/rules.d/`
1. reboot
1. python3 main.py

# 起動手順
1. python3 main.py

