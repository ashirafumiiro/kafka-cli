import argparse
import app


def read_args():
    ''' 
    Returns a dictionary containing the args'''
    parser = argparse.ArgumentParser()
    parser.add_argument("command", help="Command", choices=['send', 'receive'])
    parser.add_argument('--channel', help="Topic to be included", required=True)
    parser.add_argument('--kafka', help="Kafka connection string", required=True)
    parser.add_argument('--from', help="The point to start receiving messages from", 
                        choices=['start', 'latest'])
    args = parser.parse_args()
    return vars(args)


if __name__ == '__main__':
    args_dict = read_args()
    if app.check_args(args_dict):
        if args_dict['command'] == 'send':
            app.send_message(args_dict, "hello world")
        elif args_dict['command'] == 'receive':
            app.read_messages(args_dict)