FROM ubuntu:latest

RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python2.7 \
    portaudio19-dev \
    ffmpeg

# Set working directory
WORKDIR /app

# Copy requirements files
COPY requirements.txt .

# Install Python 2.7 dependencies
#RUN pip2 install --no-cache-dir -r requirements.txt

# Install Python 3 dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .


# Need to make this script run when container is started, maybe from command in docker-compose.yml?
#RUN sh -c ./activate.sh
