# gpt-tools

## 関連リポジトリ

[https://github.com/ayataka0nk/gpt-tools-web](https://github.com/ayataka0nk/gpt-tools-web)

[https://github.com/ayataka0nk/gpt-tools](https://github.com/ayataka0nk/gpt-tools)

## ディレクトリ構成

ベースはこれでやってみる
https://github.com/zhanymkanov/fastapi-best-practices

service は増えてくはずなのでさすがに services として別に切る

## エディタ環境構築作業メモ？

拡張機能 Flake8 をインストール

下記コマンドで autopep8 をエディタから見える python 環境にインストール。vscode 拡張機能の autopep8 はなぜか動かなかったので使わない。
↓、venv 使う場合は不要

```
pip install autopep8
```

## python 環境として docker を使わない場合

wsl での構築方法。linux でも同じはず。mac は引っかかるポイントあるかも。

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

mysqlclient のインストール絡みでこの辺が必要になるかも。

```
apt -y install libmysqlclient-dev python3.11-dev
```

ローカル用開発サーバを立てるのはこう。

```
uvicorn app.main:app --reload
```

## たまに使うコマンドメモ

### マイグレーション作成

```
alembic revision -m "名前"
```

### マイグレーション適用

```
alembic upgrade head
alembic upgrade +1
```

```
alembic downgrade base
alembic downgrade -1
```
