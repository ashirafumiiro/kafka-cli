import argparse
import app


if __name__ == '__main__':
    args_dict = app.read_args()
    
    if args_dict['command'] == 'send':
        app.send_message(args_dict)
    elif args_dict['command'] == 'receive':
        app.read_messages(args_dict)