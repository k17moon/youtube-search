# python:3.8をベースとします
FROM python:3.8
# 環境変数 PYTHONUNBUFFEREDを設定
ENV PYTHONUNBUFFERED 1
# mkdirコマンドの実行
RUN mkdir /code
# 作業ディレクトリの設定
WORKDIR /code
# requirements.txtを/codeに追加する
ADD requirements.txt /code/
# Pythonのパッケージ管理ツールのpipをアップグレード
RUN pip install --upgrade pip
# pipでrequirements.txtに指定されているパッケージを追加する
RUN pip install -r requirements.txt
# ローカルのディレクトリを/codeに追加する
ADD . /code/