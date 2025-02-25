import pika
import logging
import sys
import argparse
from argparse import RawTextHelpFormatter
from time import sleep

def on_message(channel, method_frame, header_frame, body):
    """ Callback function to process received messages """
    print(f"Received Message: {body.decode('utf-8')}")
    LOG.info('Message has been received: %s', body.decode('utf-8'))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


if __name__ == '__main__':
    examples = f"{sys.argv[0]} -p 5672 -s rabbitmq"

    parser = argparse.ArgumentParser(
        formatter_class=RawTextHelpFormatter,
        description="Run consumer.py",
        epilog=examples
    )
    parser.add_argument('-p', '--port', required=True, help="The port to listen on.")
    parser.add_argument('-s', '--server', required=True, help="The RabbitMQ server.")

    args = parser.parse_args()

    # Sleep to allow RabbitMQ to start
    sleep(5)

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
    channel.queue_declare(queue='pc')

    # Fix: Correct argument order for basic_consume
    channel.basic_consume(queue='pc', on_message_callback=on_message)

    try:
        LOG.info("Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    except KeyboardInterrupt:
        LOG.info("Stopping consumer...")
        channel.stop_consuming()
    finally:
        connection.close()
        LOG.info("Connection closed.")
