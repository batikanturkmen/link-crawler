from confluent_kafka import Producer
from confluent_kafka import Consumer
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import config

conf = {'bootstrap.servers': config.bootstrap_servers,
        'client.id': config.worker_client_id}

producer = Producer(conf)

ssl._create_default_https_context = ssl._create_unverified_context

conf = {'bootstrap.servers': config.bootstrap_servers,
        'group.id': config.worker_group_id,
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
consumer.subscribe([config.links_to_be_processed_topic])


def write_to_kafka(topic, key, value):
    encoded_key = bytes(key, encoding='utf-8')
    encoded_value = bytes(value, encoding='utf-8')
    producer.produce(topic, key=encoded_key, value=encoded_value)


def kafka_record_to_key_value(record):
    transformed_key = record.key().decode("utf-8")
    transformed_value = record.value().decode("utf-8")

    return transformed_key, transformed_value


try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        else:
            _, link_to_be_crawled = kafka_record_to_key_value(msg)
            req = Request(link_to_be_crawled)
            response = None
            try:
                response = urlopen(req)
            except:
                continue
            soup = BeautifulSoup(response.read(), "lxml")
            for link in soup.findAll('a'):
                full_url = link.get('href')
                if full_url is not None:
                    print('Worker Full URL: ' + full_url)
                    write_to_kafka(config.processed_links_topic,
                                   key=link_to_be_crawled,
                                   value=full_url)
finally:
    # Close down consumer to commit final offsets.
    consumer.close()
