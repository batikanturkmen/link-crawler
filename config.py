# neo4j configuration
import os
neo4j_database_address = 'bolt://neo4j:7687'
neo4j_database_username = 'neo4j'
neo4j_database_password = 'batikan'

# kafka configuration
links_to_be_processed_topic = 'links_to_be_processed'
links_to_be_processed_topic_num_partitions = 3
links_to_be_processed_topic_replication_factor = 1
processed_links_topic = 'processed_link'
processed_links_topic_num_partitions = 3
processed_links_topic_replication_factor = 1
master_group_id = 'master_group'
master_client_id = 'master_client'
worker_group_id = 'worker_group'
worker_client_id = 'worker_client'
topic_creator_group_id = 'creator_group'
bootstrap_servers = 'kafka-cluster:9092'

