from confluent_kafka import Producer
from confluent_kafka import Consumer

import urllib.parse
import tldextract
import persister
import config

# neo4j connection
# TODO
# neo4jsession = persister.NeoDatabase(config.neo4j_database_address,
#                                     config.neo4j_database_username,
#                                     config.neo4j_database_password)

# TODO mailto olayi ve pdf olayı eğer bunlar varsa master göndermeyecek
# TODO kafkanın problemi
# TODO dockerize
# TODO readme

base_domain = 'https://www.afiniti.com/'  # TODO parametrik al
main_domain = tldextract.extract(base_domain).domain

processed_topics = []  # TODO ilk açılışta doldur bunu


def write_to_kafka(topic, key, value):
    encoded_key = bytes(key, encoding='utf-8')
    encoded_value = bytes(value, encoding='utf-8')
    producer.produce(topic, key=encoded_key, value=encoded_value)


def kafka_record_to_key_value(record):
    transformed_key = record.key().decode("utf-8")
    transformed_value = record.value().decode("utf-8")
    transformed_key = urllib.parse.urljoin(base_domain, transformed_key)
    transformed_value = urllib.parse.urljoin(base_domain, transformed_value)

    return transformed_key, transformed_value


# def add_to_graph(source_link, destination_link):
#    neo4jsession.link_urls(source_link, destination_link)


conf = {'bootstrap.servers': config.bootstrap_servers,
        'client.id': config.master_client_id}

producer = Producer(conf)


conf = {'bootstrap.servers': config.bootstrap_servers,
        'group.id': config.master_group_id,
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
consumer.subscribe([config.processed_links_topic])

write_to_kafka(topic=config.links_to_be_processed_topic,
               key=base_domain,
               value=base_domain)

processed_topics.append(base_domain)

try:
    while True:
        msg = consumer.poll(timeout=1.0)
        if msg is None:
            continue
        if msg.error():
            continue
        else:
            source, destination = kafka_record_to_key_value(msg)

            print("Master recieved source : " + source)
            print("Master recieved destination : " + destination)

            if destination not in processed_topics \
                    and tldextract.extract(destination).domain == main_domain:  # check domain is belong to crawled link
                write_to_kafka(topic=config.links_to_be_processed_topic,
                               key=destination,
                               value=destination)
                print("Added to processed topics : " + destination)
                # add_to_graph(source, destination)
                processed_topics.append(destination)
                print("current processed nodes count: " + str(len(processed_topics)))
finally:
    # Close down consumer to commit final offsets.
    consumer.close()

#neo4jsession.close() #TODO
