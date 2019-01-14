FROM ubuntu:latest
RUN apt-get update && apt-get install -y \
   python3 \
   python3-pip \
  python3-dev 
WORKDIR /app
COPY . /app
RUN pip3 install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python3"]
CMD ["message_classifier.py"]
