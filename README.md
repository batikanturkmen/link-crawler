### Link Crawler

The aim of this project is to extract and graph all the links that
can be reached through the given link.

#### Requirements

- Docker

#### Run

Project can run with `docker-compose up` command.

For terminating project you can use `docker-compose up` command.
If you make change on python files, you have to rerun dockerization stages without using cache. 
`docker-compose build --no-cache crawler-master crawler-worker` command can be used for no-cache re-build

#### Project outline

![Project outline](assets/pipeline-v1.png)

##### Master Node

Master node is responsible for writing links that to be crawled to the kafka topic.
Moreover, it processes responses of worker nodes, and write them to the graph database.

##### Worker Node(s)

Worker nodes are dummy and size of these can be increased to achieve better performance.
These nodes read links to be crawled kafka topic, crawl and write its findings to different kafka topic.

##### Communication

[Apache Kafka](https://kafka.apache.org/) is used as message broker.
Kafka Cluster and related components can be monitored and managed by Landoop UI at `http://localhost:3030/`. This UI helps us to see topics, schemas and connectors.

![Kafka UI](assets/landoop-ui.png)

Kafka consumer groups helps us to distribute messages among workers with respect to [round robin](https://en.wikipedia.org/wiki/Round-robin_scheduling).
On the other hand, we have to create multiple partition (in our case it is 3) to support multiple workers.
According to the architecture of the Kafka, a partition can be consumed by only one consumer, while a consumer can consume more than one partition.

##### Storage

To be able to store and present connections, this project is using [neo4j](https://neo4j.com/) graph databases.
neo4j has web interface in it that helps both querying and presenting the stored data.

Example graph output can be seen as follows;


![Link graph outline](assets/graph-v1.png)


##### Database usage

You can access neo4j database ui at [http://localhost:7474/](http://localhost:7474/) (username: neo4j, password: batikan) 
and use following query to see whole graph;

```
MATCH(node)
RETURN node
```

You can also interact with graph nodes and see how to connect each other as follows.

![Single graph outline](assets/graph-single-node.png)

Query of upper image is:

```
MATCH(s:URL{link: 'https://www.afiniti.com/'})
RETURN s
```

After running query you should click node -> expand to see connected nodes.

#### Future Works

- Add multi-stage build to reduce docker image sizes.