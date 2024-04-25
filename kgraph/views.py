import matplotlib.pyplot as plt
import matplotlib
# from .predict.predict import *
from django.http import JsonResponse, FileResponse
from django.views.decorators.csrf import csrf_exempt
import io
import json
from django.shortcuts import render
from neo4j import GraphDatabase
from py2neo import Graph
# Create your views here.
# 连接neo4j数据库
driver = GraphDatabase.driver(
    "neo4j://127.0.0.1:7687", auth=("neo4j", "123456lcyjy"))
graph = Graph("neo4j://localhost:7474", auth=("neo4j", "123456lcyjy"))


matplotlib.use('Agg')

# # 连接Neo4j数据库
# driver = GraphDatabase.driver(
#     "bolt://localhost:7687", auth=("neo4j", "123456789"))
# graph = Graph("bolt://localhost:7687", auth=("neo4j", "123456789"))


@csrf_exempt
def img(request):
    # 绘制图形
    plt.plot([1, 2, 3, 4], [1, 4, 9, 16])
    plt.xlabel('x-axis')
    plt.ylabel('y-axis')

    # 保存图像为 BytesIO 对象
    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)

    print('****************************************************************')
    print(img_buffer)
    # 返回图像数据给前端
    return FileResponse(img_buffer, content_type='image/png')

# 预测模块的
# @csrf_exempt
# def predict_image(request):
#     if request.method == "POST":
#         # 前端向后端发送的参数  data = request.get_json(silent=True)
#         data = json.loads(request.body)
#         feature_cols = data["feature_col"]
#         target_cols = data["target_col"]
#         print(feature_cols)
#         print(target_cols)

#         train_x, test_x, train_y, test_y = divide(feature_cols, target_cols)
#         rfr = RandomForestRegressor()

#         buffer = evaluate_image(feature_cols, target_cols, train_x, train_y, test_x, test_y,
#                                 "Features", rfr)
#         print(buffer)
#         # 返回图像数据给前端
#         return FileResponse(buffer, content_type='image/png')


# @csrf_exempt
# def predict_data(request):
#     if request.method == "POST":
#         # 前端向后端发送的参数  data = request.get_json(silent=True)
#         data = json.loads(request.body)
#         feature_cols = data["feature_col"]
#         target_cols = data["target_col"]

#         train_x, test_x, train_y, test_y = divide(feature_cols, target_cols)
#         rfr = RandomForestRegressor()

#         rmse, mae, mse, r2 = evaluate_data(feature_cols, target_cols, train_x, train_y, test_x, test_y,
#                                            "Features", rfr)

#         data = [rmse, mae, mse, r2]
#         print(data)
#         # 返回图像数据给前端
#         # return '1'
#         return JsonResponse(data, safe=False)


@csrf_exempt
def search(request):
    if request.method == "POST":
        # 前端向后端发送的参数  data = request.get_json(silent=True)
        data = json.loads(request.body)
        n_node = data["nNodeList"]
        rel = data["relList"]
        m_node = data["mNodeList"]
        print(n_node)
        print(rel)
        print(m_node)

        dict1 = dataProcessing(n_node, rel, m_node)
        print(dict1)
        return JsonResponse(dict1, safe=False)


def dataProcessing(Nnode, Rel, Mnode):
    nodes = []
    links = []
    nodes_set = []
    if Nnode[0] is None or Nnode[0] == '':
        n_node = ''
    else:
        n_node = ':`' + str(Nnode[0]) + '`'

    if Rel[0] is None or Rel[0] == '':
        rel = ''
    else:
        rel = ':`' + str(Rel[0]) + '`'

    if Mnode[0] is None or Mnode[0] == '':
        m_node = ''
    else:
        m_node = ':`' + str(Mnode[0]) + '`'

    print("n_node: " + n_node + " rel: " + rel + " m_node: " + m_node)

    with driver.session() as session:
        # <Record source=50 source_labels=['硅灰基因'] source_properties={'Silica_index': 26, 'name': 'Silica'} target=51 target_labels=['碳化基因'] target_properties={'name': 'Carbonization', 'Carbonization_index': 26} link=690 r_type='预测' r_properties={}>
        result = session.run(
            'MATCH (n' + n_node + ')-[r' + rel + ']->(m' + m_node + ') RETURN ' +
            'id(n) as source, labels(n) as source_labels, properties(n) as source_properties, ' +
            'id(m) as target, labels(m) as target_labels, properties(m) as target_properties, ' +
            'id(r) as link, type(r) as r_type, properties(r) as r_properties ' +
            'LIMIT 300')

        for record in result:
            nodes.append({"id": record['source'], "label": record['source_labels'][0],
                          "properties": record['source_properties']})
            nodes.append({"id": record['target'], "label": record['target_labels'][0],
                          "properties": record['target_properties']})
            links.append({"source": record['source'], "target": record['target'], "type": record['r_type'],
                          "properties": record['r_properties']})

        for i in nodes:
            if i not in nodes_set:
                nodes_set.append(i)
        result_dict = dict(zip(['nodes', 'links'], [nodes_set, links]))
        # print(result_dict)
        return result_dict
