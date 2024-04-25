from django.shortcuts import render

# Create your views here.
import pandas as pd
from py2neo import Node, Graph, Relationship, NodeMatcher, Subgraph
from django.http import HttpResponse


def get_csv_list(data):
    # 原始数据（先取前面30个数据（Neo4j图数据库存储不了那么多数据））
    origin_data = pd.read_csv(
        'D:\\pythonProject\\school\\djangoProject\\Test\\kgraph\\data\\USTB_carbon.csv', header=1, nrows=30)
    # 填补缺失值
    origin_data.fillna(0, inplace=True)
    print(origin_data)
    # 连接到Neo4j数据库
    graph = Graph("http://localhost:7474",
                  user="neo4j", password="123456lcyjy")
    # graph = Graph("http://localhost:7474", auth=("neo4j", "123456LCYjy"))
    # 清空数据库
    graph.delete_all()
    # 读取csv中的数据
    # 遍历数据帧中的每一行
    for index, row in origin_data.iterrows():
        # 创建一个新的节点
        # node = Node("NodeLabel", name=row['name'],
        #             property1=row['property1'], property2=row['property2'])
        # # 将节点添加到图中
        # graph.create(node)

        # 添加水泥节点
        # 使用MERGE命令创建节点,节点不存在则创建新节点,存在则返回节点
        node_cement = Node("水泥", name="水泥", cement_index=index)
        graph.create(node_cement)
        graph.run("""MERGE (n:C_CaO {name: $name, value: $property1})""",
                  name="CaO", property1=row['C-Ca'])
        graph.run("""MERGE (n:C_SiO {name: $name, value: $property1})""",
                  name="SiO", property1=row['C-Si'])
        graph.run("""MERGE (n:C_Al2O3 {name: $name, value: $property1})""",
                  name="Al2O3", property1=row['C-Al'])
        graph.run("""MERGE (n:C_MgO {name: $name, value: $property1})""",
                  name="MgO", property1=row['C-Mg'])
        graph.run("""MERGE (n:C_Fe2O3 {name: $name, value: $property1})""",
                  name="Fe2O3", property1=row['C-Fe'])
        graph.run("""MERGE (n:水泥强度 {name: $name, value: $property1})""",
                  name="水泥强度", property1=row['strength'])
        graph.run("""MERGE (n:单方水泥用量 {name: $name, value: $property1})""",
                  name="单方水泥用量", property1=row['cement'])
        # 创建关系
        graph.run("""
        MATCH (a:C_CaO {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="CaO", property1=row['C-Ca'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:C_SiO {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="SiO", property1=row['C-Si'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:C_Al2O3 {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Al2O3", property1=row['C-Al'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:C_MgO {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="MgO", property1=row['C-Mg'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:C_Fe2O3 {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Fe2O3", property1=row['C-Fe'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:水泥强度 {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="水泥强度", property1=row['strength'], name_0="水泥", property_0=index)
        graph.run("""
        MATCH (a:单方水泥用量 {name: $name, value: $property1}), (b:水泥 {name: $name_0, cement_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="单方水泥用量", property1=row['cement'], name_0="水泥", property_0=index)

        # 添加粉煤灰节点
        node_FA = Node("粉煤灰", name="FA", FA_index=index)
        graph.create(node_FA)
        graph.run("""MERGE (n:FA_CaO {name: $name, value: $property1})""",
                  name="CaO", property1=row['FA-Ca'])
        graph.run("""MERGE (n:FA_SiO {name: $name, value: $property1})""",
                  name="SiO", property1=row['FA-Si'])
        graph.run("""MERGE (n:FA_Al2O3 {name: $name, value: $property1})""",
                  name="Al2O3", property1=row['FA-Al'])
        graph.run("""MERGE (n:FA_MgO {name: $name, value: $property1})""",
                  name="MgO", property1=row['FA-Mg'])
        graph.run("""MERGE (n:FA_Fe2O3 {name: $name, value: $property1})""",
                  name="Fe2O3", property1=row['FA-Fe'])
        graph.run("""MERGE (n:一级粉煤灰用量 {name: $name, value: $property1})""",
                  name="一级粉煤灰用量", property1=row['FA-1'])
        graph.run("""MERGE (n:二级粉煤灰用量 {name: $name, value: $property1})""",
                  name="二级粉煤灰用量", property1=row['FA-2'])
        # 创建关系
        graph.run("""
        MATCH (a:FA_CaO {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="CaO", property1=row['FA-Ca'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:FA_SiO {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="SiO", property1=row['FA-Si'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:FA_Al2O3 {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Al2O3", property1=row['FA-Al'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:FA_MgO {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="MgO", property1=row['FA-Mg'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:FA_Fe2O3 {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Fe2O3", property1=row['FA-Fe'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:一级粉煤灰用量 {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="一级粉煤灰用量", property1=row['FA-1'], name_0="FA", property_0=index)
        graph.run("""
        MATCH (a:二级粉煤灰用量 {name: $name, value: $property1}), (b:粉煤灰 {name: $name_0, FA_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="二级粉煤灰用量", property1=row['FA-2'], name_0="FA", property_0=index)

        # 添加矿渣节点
        node_Slag = Node("矿渣", name="Slag", Slag_index=index)
        graph.create(node_Slag)
        graph.run("""MERGE (n:Slag_CaO {name: $name, value: $property1})""",
                  name="CaO", property1=row['Slag-Ca'])
        graph.run("""MERGE (n:Slag_SiO {name: $name, value: $property1})""",
                  name="SiO", property1=row['Slag-Si'])
        graph.run("""MERGE (n:Slag_Al2O3 {name: $name, value: $property1})""",
                  name="Al2O3", property1=row['Slag-Al'])
        graph.run("""MERGE (n:Slag_MgO {name: $name, value: $property1})""",
                  name="MgO", property1=row['Slag-Mg'])
        graph.run("""MERGE (n:Slag_Fe2O3 {name: $name, value: $property1})""",
                  name="Fe2O3", property1=row['Slag-Fe'])
        graph.run("""MERGE (n:矿渣用量 {name: $name, value: $property1})""",
                  name="矿渣用量", property1=row['Slag'])
        # 创建关系
        graph.run("""
        MATCH (a:Slag_CaO {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="CaO", property1=row['Slag-Ca'], name_0="Slag", property_0=index)
        graph.run("""
        MATCH (a:Slag_SiO {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="SiO", property1=row['Slag-Si'], name_0="Slag", property_0=index)
        graph.run("""
        MATCH (a:Slag_Al2O3 {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Al2O3", property1=row['Slag-Al'], name_0="Slag", property_0=index)
        graph.run("""
        MATCH (a:Slag_MgO {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="MgO", property1=row['Slag-Mg'], name_0="Slag", property_0=index)
        graph.run("""
        MATCH (a:Slag_Fe2O3 {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="Fe2O3", property1=row['Slag-Fe'], name_0="Slag", property_0=index)
        graph.run("""
        MATCH (a:矿渣用量 {name: $name, value: $property1}), (b:矿渣 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="矿渣用量", property1=row['Slag'], name_0="Slag", property_0=index)

        # 石灰石粉
        node_Lsp = Node("石灰石", name="Lsp", Lsp_index=index)
        graph.create(node_Lsp)
        graph.run("""MERGE (n:Ca_powder {name: $name, value: $property1})""",
                  name="石灰石粉", property1=row['Ca-powder'])
        graph.run("""
        MATCH (a:Ca_powder {name: $name, value: $property1}), (b:石灰石 {name: $name_0, Lsp_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="石灰石粉", property1=row['Ca-powder'], name_0="Lsp", property_0=index)

        # 硅灰
        node_Silica = Node("硅灰", name="Silica", Silica_index=index)
        graph.create(node_Silica)
        graph.run("""MERGE (n:Si_surface {name: $name, value: $property1})""",
                  name="硅灰比表面积", property1=row['Si-surface'])
        graph.run("""MERGE (n:Si_powder {name: $name, value: $property1})""",
                  name="硅灰用量", property1=row['Si-powder'])
        graph.run("""
        MATCH (a:Si_surface {name: $name, value: $property1}), (b:硅灰 {name: $name_0, Silica_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="硅灰比表面积", property1=row['Si-surface'], name_0="Silica", property_0=index)
        graph.run("""
        MATCH (a:Si_powder {name: $name, value: $property1}), (b:硅灰 {name: $name_0, Silica_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="硅灰用量", property1=row['Si-powder'], name_0="Silica", property_0=index)

        # 预测结果
        node_Carbonization = Node(
            "碳化基因", name="Carbonization", Carbonization_index=index)
        graph.create(node_Carbonization)
        graph.run("""MERGE (n:C28天强度 {name: $name, value: $property1})""",
                  name="strength28d", property1=row['strength28d'])
        graph.run("""MERGE (n:碳化开始时间 {name: $name, value: $property1})""",
                  name="begintime", property1=row['begintime'])
        graph.run("""MERGE (n:碳化持续时间 {name: $name, value: $property1})""",
                  name="holdtime", property1=row['holdtime'])
        graph.run("""MERGE (n:碳化深度 {name: $name, value: $property1})""",
                  name="deepth", property1=row['deepth'])

        # 创建关系
        graph.run("""
        MATCH (a:C28天强度 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Carbonization_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="strength28d", property1=row['strength28d'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:碳化开始时间 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Carbonization_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="begintime", property1=row['begintime'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:碳化持续时间 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Carbonization_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """, name="holdtime", property1=row['holdtime'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:碳化深度 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Carbonization_index: $property_0})
        MERGE (a)-[r:组成]->(b)
        """,  name="deepth", property1=row['deepth'], name_0="Carbonization", property_0=index)

        # 添加单节点
        # 用水量 水灰比 (粗骨料用量 细骨料用量)
        graph.run("""MERGE (n:用水量 {name: $name, value: $property1})""",
                  name="water", property1=row['water'])
        graph.run("""MERGE (n:水灰比 {name: $name, value: $property1})""",
                  name="ratio", property1=row['ratio'])

        graph.run("""MERGE (n:粗骨料用量 {name: $name, value: $property1})""",
                  name="粗骨料用量", property1=row['bigagregate'])
        graph.run("""MERGE (n:细骨料用量 {name: $name, value: $property1})""",
                  name="细骨料用量", property1=row['smallagregate'])

        # 预测关系
        rel1 = Relationship(node_cement, "预测", node_Carbonization)
        graph.create(rel1)
        rel2 = Relationship(node_FA, "预测", node_Carbonization)
        graph.create(rel2)
        rel3 = Relationship(node_Slag, "预测", node_Carbonization)
        graph.create(rel3)
        rel4 = Relationship(node_Lsp, "预测", node_Carbonization)
        graph.create(rel4)
        rel5 = Relationship(node_Silica, "预测", node_Carbonization)
        graph.create(rel5)

        graph.run("""
        MATCH (a:用水量 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:预测]->(b)
        """, name="water", property1=row['water'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:水灰比 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:预测]->(b)
        """, name="ratio", property1=row['ratio'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:粗骨料用量 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:预测]->(b)
        """, name="粗骨料用量", property1=row['bigagregate'], name_0="Carbonization", property_0=index)
        graph.run("""
        MATCH (a:细骨料用量 {name: $name, value: $property1}), (b:碳化基因 {name: $name_0, Slag_index: $property_0})
        MERGE (a)-[r:预测]->(b)
        """,  name="细骨料用量", property1=row['smallagregate'], name_0="Carbonization", property_0=index)
    # return HttpResponse("添加数据成功.")
