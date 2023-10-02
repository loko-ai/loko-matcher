FROM python:3.10-slim
EXPOSE 8080
ADD ./requirements.txt /
RUN pip install -r /requirements.txt
ARG GATEWAY
ENV GATEWAY=$GATEWAY
ADD . /plugin
ENV PYTHONPATH=$PYTHONPATH:/plugin
WORKDIR /plugin/services
#HEALTHCHECK --interval=5s --timeout=60s CMD python /plugin/utils/healtcheck.py
CMD python services.py