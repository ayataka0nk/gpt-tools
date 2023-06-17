# gpt-tools

## ディレクトリ構成

ベースはこれでやってみる
https://github.com/zhanymkanov/fastapi-best-practices

serviceは増えてくはずなのでさすがにservicesとして別に切る

## エディタ環境構築作業メモ？

拡張機能Flake8をインストール

下記コマンドでautopep8をエディタから見えるpython環境にインストール。vscode拡張機能のautopep8はなぜか動かなかったので使わない。
```
pip install autopep8
```

## python環境としてdockerを使わない場合

wslでの構築方法。linuxでも同じはず。macは引っかかるポイントあるかも。

```
# 自環境に合ったやり方でpython3.11とvenvをインストール
sudo apt install python3.11 python3.11-venv
```

プロジェクトルートで
```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

何か新しくインストールしたときは

```
pip freeze > requirements.txt
```

mysqlclientのインストール絡みでこの辺が必要になるかも。
```
apt -y install libmysqlclient-dev python3.11-dev
```