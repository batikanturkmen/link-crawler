from neo4j import GraphDatabase


class NeoDatabase:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def link_urls(self, source, destination):
        with self.driver.session() as session:
            session.write_transaction(self._create_connection, source, destination)

    @staticmethod
    def _create_connection(tx, source, destination):
        result = tx.run(
            "MERGE (s:URL{link: $source}) MERGE (d:URL{link: $destination}) MERGE (s)-[:DIRECTS]->(d) RETURN s, d",
            source=source,
            destination=destination)
        return result.single()
