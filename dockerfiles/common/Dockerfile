#全てのライブラリを補完しているver3.7をインストール
FROM python:3.8
USER root

#日本語のドキュメント
RUN apt-get update
RUN apt-get -y install locales && \
    localedef -f UTF-8 -i ja_JP ja_JP.UTF-8
ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

RUN mkdir -p /root/opt
COPY . /root/opt
# COPY requirements.txt /root/opt
WORKDIR /root/opt
EXPOSE 8501

RUN apt-get install -y vim less
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
#versionの指定を行った、requirements.txtのダウンロード
#最初はtxtでインストールを行い、完全にversionを合わせるためにpip freeze > requirements.lockに落とし込む
RUN pip install -r requirements.lock
# RUN pip install -r requirements.txt



