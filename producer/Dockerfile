FROM python:3.9

ENV PYTHONPATH /usr/src/app

WORKDIR /app

ADD producer.py /app
ADD requirements.txt /app

RUN pip install --requirement /app/requirements.txt

# Update and install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dnsutils \
    iputils-ping \
    net-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

#CMD ["python3", "producer.py", "-p", "5672", "-s", "rabbitmq-service", "-m", "Hello" ,"-r" , 30 ]
# python3 producer.py -p 5672 -s rabbitmq-service -m Hello -r 30