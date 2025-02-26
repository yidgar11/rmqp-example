import pika
import logging
import sys
import argparse
from argparse import RawTextHelpFormatter
from time import sleep
from datetime import datetime

if __name__ == '__main__':
    examples = f"{sys.argv[0]} -p 5672 -s rabbitmq -m 'Hello'"

    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Run producer.py",
        epilog=examples
    )
    parser.add_argument('-p', '--port', required=True, help="The port to listen on.")
    parser.add_argument('-s', '--server', required=True, help="The RabbitMQ server.")
    parser.add_argument('-m', '--message', default='Hello', help="The message to send.")
    parser.add_argument('-r', '--repeat', type=int, default=30, help="Number of times to repeat the message.")

    args = parser.parse_args()

    # Sleep to allow RabbitMQ to start
    sleep(30)

    # Configure logging
    logging.basicConfig(level=logging.INFO)
    LOG = logging.getLogger(__name__)

    # RabbitMQ connection parameters
    credentials = pika.PlainCredentials('guest', 'guest')
    parameters = pika.ConnectionParameters(
        host=args.server,
        port=int(args.port),
        virtual_host='/',
        credentials=credentials
    )

    # Establish connection
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()

    # Declare the queue
    queue = channel.queue_declare(queue='pc')
    queue_name = queue.method.queue

    # Enable delivery confirmation
    channel.confirm_delivery()

    # Publish messages
    for i in range(args.repeat):
        send_time = datetime.now().strftime('%H:%M:%S')
        message = f"[{send_time}]-args.message"
        if channel.basic_publish(exchange='', routing_key=queue_name, body=message):
            LOG.info(f"Message {i+1} delivered: {args.message}")
        else:
            LOG.warning(f"Message {i+1} NOT delivered!")

        sleep(2)

    connection.close()
    LOG.info("Connection closed.")
