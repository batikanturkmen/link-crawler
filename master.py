from kafka import KafkaProducer
from kafka import KafkaConsumer
import urllib.parse
import tldextract
import persister
import config

# neo4j connection
neo4jsession = persister.NeoDatabase(config.neo4j_database_address,
                                     config.neo4j_database_username,
                                     config.neo4j_database_password)

# TODO mailto olayi
# TODO hem .com/ var hem .com
# TODO replicaton factorlu topicleri acarsin

base_domain = 'https://www.afiniti.com/' # TODO parametrik al
main_domain = tldextract.extract(base_domain).domain  # TODO

processed_topics = []  # TODO ilk açılışta doldur bunu


def write_to_kafka(topic, key, value):
    encoded_key = bytes(key, encoding='utf-8')
    encoded_value = bytes(value, encoding='utf-8')
    producer_future = producer.send(topic, key=encoded_key, value=encoded_value)
    metadata = producer_future.get(timeout=10)
    return metadata


def kafka_record_to_key_value(record):
    transformed_key = record.key.decode("utf-8")
    transformed_value = record.value.decode("utf-8")
    transformed_key = urllib.parse.urljoin(base_domain, transformed_key)
    transformed_value = urllib.parse.urljoin(base_domain, transformed_value)

    return transformed_key, transformed_value


def add_to_graph(source_link, destination_link):
    neo4jsession.link_urls(source_link, destination_link)


producer = KafkaProducer(bootstrap_servers=config.bootstrap_servers)
consumer = KafkaConsumer(config.processed_links_topic,
                         group_id=config.master_group_id)

write_to_kafka(topic=config.links_to_be_processed_topic,
               key=base_domain,
               value=base_domain)
processed_topics.append(base_domain)

for msg in consumer:
    source, destination = kafka_record_to_key_value(msg)

    print("Master recieved source : " + source)
    print("Master recieved destination : " + destination)

    if destination not in processed_topics \
            and tldextract.extract(destination).domain == main_domain:  # check domain is belong to given link
        write_to_kafka(topic=config.links_to_be_processed_topic,
                       key=destination,
                       value=destination)
        print("Added to processed topics : " + destination)
        add_to_graph(source, destination)
        processed_topics.append(destination)
        print("current processed nodes count: " + str(len(processed_topics)))

neo4jsession.close()

