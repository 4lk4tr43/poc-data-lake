from json import dumps
from os import environ
from socket import gethostname
from confluent_kafka import Producer
from flask import Flask, request
from flask_cors import CORS

app = Flask(__name__)
producer = Producer(
    {'bootstrap.servers': environ['KAFKA_HOSTS'], 'client.id': gethostname()})

CORS(app)


@app.route('/', methods=['GET'])
def home():
    return 'Queue Receiver', 200


@app.route('/store', methods=['POST'])
def store():
    producer.produce(environ['TOPIC'], dumps(request.json))
    return '', 204


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
