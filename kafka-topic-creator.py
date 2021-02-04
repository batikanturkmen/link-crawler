from kafka import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic
import config

topic_list = []

client = KafkaClient(bootstrap_servers=config.bootstrap_servers)
admin_client = KafkaAdminClient(
    bootstrap_servers=config.bootstrap_servers,
    client_id=config.topic_creator_group_id
 )

future = client.cluster.request_update()
client.poll(future=future)

metadata = client.cluster
print(metadata.topics())

if config.links_to_be_processed_topic not in metadata.topics():
    print("creating " + config.links_to_be_processed_topic)
    topic_list.append(NewTopic(name=config.links_to_be_processed_topic,
                               num_partitions=config.links_to_be_processed_topic_num_partitions,
                               replication_factor=config.links_to_be_processed_topic_replication_factor))

if config.processed_links_topic not in metadata.topics():
    print("creating " + config.processed_links_topic)
    topic_list.append(NewTopic(name=config.processed_links_topic,
                               num_partitions=config.processed_links_topic_num_partitions,
                               replication_factor=config.processed_links_topic_replication_factor))

creation_response = admin_client.create_topics(new_topics=topic_list, validate_only=False)
print("creation response: " + str(creation_response))
