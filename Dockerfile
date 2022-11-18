FROM python:3.7-slim
RUN apt-get update --fix-missing && apt-get install -y build-essential
ADD requirements.lock /
RUN pip install --upgrade -r /requirements.lock
ADD . /ds4biz-matcher
ENV PYTHONPATH=$PYTHONPATH:/ds4biz-matcher
WORKDIR /ds4biz-matcher/ds4biz_matcher/services
EXPOSE 8080
CMD python services.py
