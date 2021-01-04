FROM ubuntu:18.04

# Install packages
RUN apt-get update
RUN apt-get install -y python3-pip postgresql-client

# Create WD
RUN mkdir -p /home/backend
WORKDIR /home/backend

# Install PIP dependencies
COPY requirements.txt /home/backend
RUN pip3 install -r requirements.txt

COPY . /home/backend

EXPOSE 5000

CMD ["python3", "app.py"]
