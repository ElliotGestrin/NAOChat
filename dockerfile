FROM ubuntu:latest

WORKDIR /app


RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python2.7 \
    portaudio19-dev \
    ffmpeg \
    wget


# Get the NAOQI-sdk
RUN wget https://community-static.aldebaran.com/resources/2.8.6/pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz

# Unzip the NAOQI-sdk
RUN tar -xf pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz -C /app

# Remove tar file
RUN rm pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz

RUN mv pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327 nao-python2.7-sdk

#RUN mv pynaoqi-python2.7-2.8.6.23-linux64-20191127_152327.tar.gz renamed.tar.gz
# Set working directory

# Copy requirements files
COPY requirements.txt .

# Install Python 2.7 dependencies
#RUN pip2 install --no-cache-dir -r requirements.txt

# Install Python 3 dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

# Copy into the dockerfile -- Should link volumes instead...
COPY . .



# Need to make this script run when container is started, maybe from command in docker-compose.yml?

#RUN chmod +x ./activate.sh
#RUN sh -c ./activate.sh
