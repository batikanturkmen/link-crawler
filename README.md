### Link Crawler

The aim of this project is to extract and graph all the links that
can be reached through the given link.

#### Requirements

- Docker

#### Run

Project can run with `docker-compose up` command.

#### Project outline

![Project outline](assets/pipeline-v1.png)

##### Master Node

Master node is responsible for writing links that to be crawled to the kafka topic.
Moreover, it processes responses of worker nodes, and write them to the graph database.

##### Worker Node(s)

Worker nodes are dummy and size of these can be increased to achieve better performance.
These nodes read links to be crawled kafka topic, crawl and write its findings to different kafka topic.

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
