FROM python:3.11

RUN apt update && apt -y install tzdata
ENV TZ=Asia/Tokyo

RUN pip3 install python-dotenv slack_bolt pytube