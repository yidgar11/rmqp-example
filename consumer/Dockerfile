FROM python:3.9

ENV PYTHONPATH /usr/src/app

WORKDIR /app

ADD consumer.py /app
ADD requirements.txt /app

# Update and install system packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    dnsutils \
    iputils-ping \
    net-tools \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN pip install --requirement /app/requirements.txt

#CMD ["python3", "consumer.py", "-p", "5672", "-s", "rabbitmq-service"]
# python3 consumer.py -p 3572 -s rabbitmq-service