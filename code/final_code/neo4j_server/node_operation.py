from py2neo import Graph, Node


# 创建节点
def create_nodes(graph,nodes):
    node_ids=[]
    for node in nodes:
        graph.create(node)
        # 获取并存储节点的ID
        node_id = node.identity
        node_ids.append(node_id)
    return node_ids


# 创建多条边
def create_relationships(graph, relationships,values):
    relationship_type="IS_TAG"
    for i in range(len(relationships)):
        source_node_id = relationships[i]["start_node_id"]
        target_node_id = relationships[i]["end_node_id"]
        value=values[i]
        # query = f"MATCH (source), (target) WHERE ID(source) = {source_node_id} AND ID(target) =" \
        #         f" {target_node_id} CREATE (source)-[:{relationship_type}]->(target)"
        query = f"MATCH (source), (target) WHERE ID(source) = {source_node_id} AND ID(target) = {target_node_id} " \
                f"CREATE (source)-[:{relationship_type} {{value: '{value}'}}]->(target)"
        graph.run(query)
