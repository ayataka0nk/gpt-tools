FROM python:3.11

ARG WWWUSER
ARG WWWGROUP

WORKDIR /work

# 依存パッケージのインストール
RUN pip install fastapi uvicorn

# 実行ユーザの作成
RUN addgroup --gid $WWWGROUP mygroup
RUN adduser --uid $WWWUSER --ingroup mygroup myuser
RUN usermod -aG sudo myuser
RUN echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers
USER myuser
