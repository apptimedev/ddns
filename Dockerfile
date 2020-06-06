FROM python:3

ADD main.py /
ADD ddns.py /

RUN pip install requests

CMD [ "python", "./main.py" ]