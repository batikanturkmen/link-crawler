import config
from confluent_kafka.admin import AdminClient, NewTopic

def create_topics():
    topics_to_be_created_list = []

    client = AdminClient({'bootstrap.servers': config.bootstrap_servers})
    topic_metadata = client.list_topics()

    if topic_metadata.topics.get(config.links_to_be_processed_topic) is None:
        print("creating " + config.links_to_be_processed_topic)
        topics_to_be_created_list.append(NewTopic(topic=config.links_to_be_processed_topic,
                                                  num_partitions=config.links_to_be_processed_topic_num_partitions,
                                                  replication_factor=config.links_to_be_processed_topic_replication_factor))

    if topic_metadata.topics.get(config.processed_links_topic) is None:
        print("creating " + config.processed_links_topic)
        topics_to_be_created_list.append(NewTopic(topic=config.processed_links_topic,
                                                  num_partitions=config.processed_links_topic_num_partitions,
                                                  replication_factor=config.processed_links_topic_replication_factor))


    if len(topics_to_be_created_list) > 0:
        # Call create_topics to asynchronously create topics. A dict
        # of <topic,future> is returned.
        fs = client.create_topics(topics_to_be_created_list)

        # Wait for each operation to finish.
        for topic, f in fs.items():
            try:
                f.result()  # The result itself is None
                print("Topic {} created".format(topic))
            except Exception as e:
                print("Failed to create topic {}: {}".format(topic, e))
