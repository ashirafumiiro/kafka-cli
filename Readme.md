# Command-line driven program that allows message exchange
This application allows you to send or receive messages from kafka cluster using the command line interface. Specifying the right arguments is handled by the `argparse` module from the python library
## Sending
In order to send, the send command is specified and the rest of the arguments added  
```bash
python main.py send --channel test --kafka localhost
```  
After the command, the user is able to type messages as they are sent to the message brokers.  

## Receiving
In order to receive the messages, the receive command is specified and in addition to the above arguments, the `--from` argument can be specified depending on whether to read the latest messages or the previous too. The help from the command line script can give further details.
```bash
python main.py send --channel test --kafka localhost --from latest
```
By default, `--from` is set to `start`

## Testing
Testing so far relies on locally installed version of apache kafka. The instance has to be running for the tests to pass