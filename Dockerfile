FROM python:alpine as builder

RUN apk update && apk add --no-cache tzdata alpine-sdk libffi-dev
ADD requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt && rm /tmp/requirements.txt

FROM python:alpine
WORKDIR /root
ENV TZ=Asia/Shanghai

COPY --from=builder /root/.local /usr/local
COPY --from=builder /usr/share/zoneinfo /usr/share/zoneinfo
COPY . /root

CMD ["python", "scheduler.py"]
