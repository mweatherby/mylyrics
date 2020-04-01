# Pull base image.
FROM frolvlad/alpine-python3
# Copy files into image
COPY . /app
# pip install required packages
RUN pip install -r /app/requirements.txt
# change starting folder of the docker image
WORKDIR /app
# Define default command.
CMD python master.py
