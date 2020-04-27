FROM balenalib/raspberrypi3-debian-python:3.7.5-buster-run
# dependencies: 
# opencv-python < 3.7
# picamera ! 3.7.6 | 3.8.1 

RUN apt-get update; \
    apt-get install -y python3-opencv

COPY requirements.txt ./
RUN pip3 install --no-cache-dir --extra-index-url=https://www.piwheels.org/simple -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["app.py"]
