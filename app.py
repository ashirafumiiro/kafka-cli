import argparse
import sys
from confluent_kafka import Producer, Consumer, KafkaError


def read_args():
    ''' 
    Returns a dictionary containing the args'''
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command", choices=['send', 'receive'])
    parser.add_argument('--channel', help="Topic to be included", required=True)
    parser.add_argument('--kafka', help="Kafka connection string", required=True)
    parser.add_argument('--from', help="The point to start receiving messages from", 
                        choices=['start', 'latest'], default='start')
    args = parser.parse_args()
    return vars(args)


def send_message(args_dict, testing=False):
    producer = Producer({'bootstrap.servers': args_dict['kafka']})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
    
    message = ''
    while message != 'q':
        if not testing:
            message = input("Enter message or 'q' to quit: ")
        else:
            message = "Test message"
        if message == 'q':
            break
    
        producer.produce(args_dict['channel'], message.encode('utf-8'), callback=delivery_report)
        producer.flush()
        if testing:
            return True
        


def read_messages(args_dict, testing=False):
    offset_config = {'start': 'earliest', 'latest': 'latest'}
    c = Consumer({
        'bootstrap.servers': args_dict['kafka'],
        'group.id': 'mygroup',
        'default.topic.config': {
            'auto.offset.reset': offset_config[args_dict['from']]  # 'smallest'
        }
    })

    c.subscribe([args_dict['channel']])
    running = True
    while running:
        msg = c.poll(1.0)

        if msg is None:
            continue
        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                continue
            else:
                print(msg.error())
                break

        print('Received message: {}'.format(msg.value().decode('utf-8')))
        if testing:
            running = False
    c.close()
    return True
