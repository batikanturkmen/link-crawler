from kafka import KafkaConsumer
from kafka import KafkaProducer
import ssl
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import config

consumer = KafkaConsumer(config.links_to_be_processed_topic,
                         group_id=config.worker_group_id)
producer = KafkaProducer(bootstrap_servers=config.bootstrap_servers)
ssl._create_default_https_context = ssl._create_unverified_context


def write_to_kafka(topic, key, value):
    encoded_key = bytes(key, encoding='utf-8')
    encoded_value = bytes(value, encoding='utf-8')
    producer_future = producer.send(topic, key=encoded_key, value=encoded_value)
    metadata = producer_future.get(timeout=10)
    return metadata


def kafka_record_to_key_value(record):
    transformed_key = record.key.decode("utf-8")
    transformed_value = record.value.decode("utf-8")

    return transformed_key, transformed_value


for msg in consumer:
    _, link_to_be_crawled = kafka_record_to_key_value(msg)
    print('Recieved from worker: ' + link_to_be_crawled)
    req = Request(link_to_be_crawled)
    response = None
    try:
        response = urlopen(req)
    except:
        continue  # TODO bu casei dusun kafkaya ne basılacak
    soup = BeautifulSoup(response.read(), "lxml")
    for link in soup.findAll('a'):
        full_url = link.get('href')
        if full_url is not None:
            print('Worker Full URL: ' + full_url)
            write_to_kafka(config.processed_links_topic,
                           key=link_to_be_crawled,
                           value=full_url)
