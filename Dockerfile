FROM python:3

RUN mkdir -p /root/src
WORKDIR /root/src

ENV LANG ja_JP.UTF-8
ENV LANGUAGE ja_JP:ja
ENV LC_ALL ja_JP.UTF-8
ENV TZ JST-9
ENV TERM xterm

ADD requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
CMD [ "python" ,"main.py"]