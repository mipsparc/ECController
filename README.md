# 概要
このソフトウェア群は、ワンハンドルマスコンと鉄道模型コントローラで鉄道模型をリアルに制御するシミュレータシステムです。

# やりたいこと
- 電車のモデルオブジェクト作成して実車に近い加減速
- udevでDSair2のポート固定

# 手順
dialoutグループにユーザーを入れる `sudo adduser $USER dialout`
udev設定をする `sudo cp udev_rules/99-dsair2.rules /etc/udev/rules.d/`
再接続
python3 main.py



