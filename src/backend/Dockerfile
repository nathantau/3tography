FROM ubuntu:18.04

# Install packages
RUN apt-get update && apt-get -y upgrade
RUN apt-get install -y python3-pip postgresql-client curl unzip
# RUN apt-get install -y curl
RUN curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && unzip awscliv2.zip && ./aws/install

# Create WD
RUN mkdir -p /home/backend
WORKDIR /home/backend

# Install PIP dependencies
COPY requirements.txt /home/backend
RUN pip3 install -r requirements.txt

COPY . /home/backend

EXPOSE 5000

CMD ["python3", "app.py"]
