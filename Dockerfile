FROM python:3.11

RUN apt update && apt -y install tzdata
ENV TZ=Asia/Tokyo

RUN apt update && apt -y install ffmpeg && \
    pip3 install python-dotenv slack_bolt pytube ffmpeg-python