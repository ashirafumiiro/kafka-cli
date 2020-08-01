import argparse
import sys
from confluent_kafka import Producer, Consumer, KafkaError


def check_args(args_dict):
    '''Checks if the command specified is valid'''
    if args_dict['command'] == 'receive':
        if args_dict['from'] == None:
            print('Add starting point')
            return False
    elif args_dict['command'] == 'send':
        pass
    else:
        return False

    return True


def send_message(args_dict, testing=False):
    producer = Producer({'bootstrap.servers': args_dict['kafka']})

    def delivery_report(err, msg):
        """ Called once for each message produced to indicate delivery result.
            Triggered by poll() or flush(). """
        if err is not None:
            print('Message delivery failed: {}'.format(err))
        else:
            print('Message delivered to {} [{}]'.format(msg.topic(), msg.partition()))
    
    message = input("Enter message or 'q' to quit: ")
    while message != 'q':
        if message == 'q':
            break
    
        producer.produce(args_dict['channel'], message.encode('utf-8'), callback=delivery_report)
        producer.flush()
        message = input("Enter message or 'q' to quit: ")


def read_messages(args_dict, testing=False):
    c = Consumer({
        'bootstrap.servers': args_dict['kafka'],
        'group.id': 'mygroup',
        'default.topic.config': {
            'auto.offset.reset': 'smallest'
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

    c.close()



if __name__ == "__main__":
    print(check_args({'command': 'send'}))
