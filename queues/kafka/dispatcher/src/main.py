from json import dumps, loads
from os import environ
from socket import socket, AF_INET, SOCK_STREAM
from urllib import request
from confluent_kafka import Consumer

processors = loads(environ['PROCESSORS']) if environ['PROCESSORS'] else []
consumer = Consumer({
    'bootstrap.servers': environ['KAFKA_HOSTS'],
    'group.id': environ['GROUP'],
    'auto.offset.reset': 'earliest'
})

consumer.subscribe([environ['TOPIC']])


def dispatch(payload):
    for processor in processors:
        do_process = True
        for attr in processor.get('mandatory'):
            if attr not in payload:
                do_process = False

        if do_process:
            body = dumps(payload).encode('utf-8')
            req = request.Request(processor.get('url'), body)
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            req.add_header('Content-Length', str(len(body)))
            if request.urlopen(processor.get('url')).getcode() == 200:
                with request.urlopen(req) as res:
                    print('Dispatched: {}'.format(processor.get('url')),
                          'Response: {}'.format(res.content))
            else:
                print('Processor {} not reachable.'.format(processor.get('url')))


while True:
    msg = consumer.poll(1.0)

    if msg is None:
        continue
    if msg.error():
        print('Consumer error: {}'.format(msg.error()))
        continue

    value = msg.value().decode('utf-8')
    print('Received message: {}'.format(value))
    dispatch(loads(value))

consumer.close()
