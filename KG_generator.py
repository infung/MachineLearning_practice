import json
from py2neo import Graph, Node, Relationship, NodeMatcher, RelationshipMatcher, ConnectionUnavailable

try:
    graph = Graph("http://localhost:7474", auth=("neo4j", "88888888"), name="neo4j")

    graph.delete_all()
    matcher_node = NodeMatcher(graph)
    matcher_relation = RelationshipMatcher(graph)

    with open("TCM-KG_triples.txt", "r", encoding="utf-8") as file:
        for line in file.readlines():
            entity_1, entity_2, relation = line.rstrip().split("\t")
            print(entity_1, "", relation, "", entity_2)
            node_1 = matcher_node.match(name=entity_1).first()
            if node_1 is None:
                if relation in ["证候", "中药", "TS_MS"]:
                    node_1 = Node("病症", name=entity_1)
                elif relation in ["功能", "药性", "部位", "贮藏", "用量", "毒性", "归经", "用法", "注意", "药味", "symmap_chemical"]:
                    node_1 = Node("中药", name=entity_1)
                elif relation in ["治法"]:
                    node_1 = Node("证候", name=entity_1)
                elif relation in ["chemical_MM"]:
                    node_1 = Node("symmap_chemical", name=entity_1)
                else:
                    node_1 = Node(name=entity_1)
                graph.create(node_1)

            node_2 = matcher_node.match(name=entity_2).first()
            if node_2 is None:
                node_2 = Node(relation, name=entity_2)
                graph.create(node_2)
            if not node_2.has_label(relation):
                node_2.add_label(relation)
                graph.push(node_2)

            r = Relationship(node_1, relation, node_2)
            graph.create(r)

except ConnectionUnavailable as e:
    print("Failed to connect to the Neo4j database.")
    print("Error message:", e)
