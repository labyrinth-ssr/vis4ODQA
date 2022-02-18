import token
from flask import (
    Flask, app, json, jsonify,request
)
from flask_cors import CORS  # 前后端分离跨域
# from attn_process import attnProcess
# from head_importance import process_impo
from functools import reduce
import re
# import ndjson
from attribution_tree_multilayer import attribution_tree


FILENAME1 = './sentence_token_pred_100.json'
FILENAME2 = './tsne_100.json'
FILENAME3 = './tsne_sentence_100.json'
FILENAME4 = './tree_data.json'
node_link_data={}
py_data2=[]
valued_nodes=[]

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


# @app.route('/query_all')
# def query_all():
#     with open(FILENAME1) as f:
#         jsonStr = json.load(f)
#         return jsonify(jsonStr)


# @app.route('/query_tsne')
# def query_tsne():
#     with open(FILENAME2) as f:
#         jsonStr = json.load(f)
#         return jsonify(jsonStr)

# @app.route('/query_sentence_tsne')
# def query_sentence_tsne():
#     with open(FILENAME3) as f:
#         jsonStr = json.load(f)
#         return jsonify(jsonStr)

# @app.route("/query_attn_head/<int:sentence_id>")
# def query_attn_head(sentence_id):
#     with open('../output/att_attr_all/att_score_zero_base_exp'+str(sentence_id)+'.json') as load_f:
#         py_data = ndjson.load(load_f)
#     with open('../output/head_importance_attr.json', 'r') as load_f2:
#         py_data2 = json.load(load_f2)
#     with open('./tokens.json', 'r') as load_f3:
#         py_data3 = json.load(load_f3)
#         return jsonify({
#             'importance': process_impo(py_data2),
#         'detail': attnProcess(py_data),
#         'tokens': py_data3
#         })
# @app.route("/query_attn_map/<int:sentence_id>")
# def query_attn_map(sentence_id):
#     with open('../output/att_attr_all/attr_zero_base_exp'+str(sentence_id)+'.json') as load_f:
#         py_data = ndjson.load(load_f)
#     return jsonify({
#         'detail': attnProcess(py_data)
#     })

@app.route('/query_attr_tree/<int:sentence_id>',methods=['GET', 'POST'])
def query_attr_tree(sentence_id):

#     global node_link_data,py_data2,valued_nodes

#     sentence_id=1;threshold=0.5;top_kth=0
#     all_layer_node_link=[]


#     # if request.method=='POST':
    
#     # post_data=request.get_json()
#     # threshold=post_data['threshold']
#     # layer=post_data['layer']
#     # attribution_tree(attr_file: str, tokens_file: str, example_index: int, threshold: int, layer: int,top_kth:int)

#     tokenPool=set()
#     f2=open('./generated_data/attr_vec/attr_vec/vec_end_'+str(sentence_id)+'.json')
#     saliency=json.loads(f2.read())

#     for i in range(0,12):
#         valued_nodes=[]
#         py_data=attribution_tree('./generated_data/attr_mat/mat_start_'+str(sentence_id)+'.json','./generated_data/tokens/input_tokens for_question'+str(sentence_id)+'.json',sentence_id,threshold,i,top_kth)
#         layerSaliency=saliency[i][top_kth]
#         with open("./generated_data/tokens/input_tokens for_question1.json", 'r') as load_f2:
#             py_data2 = json.load(load_f2)
#             py_data2=py_data2[top_kth]
#         nodes_list = []
#         links_list = []
#         def run_function(x, y): return x if y in x else x + [y]

#         for ele in py_data:
#             tar_index = ele[0].split('+')[1]
#             soc_index = ele[1].split('+')[1]
#             link_dict = {'source':
#                         soc_index, 'target': tar_index, 'value': ele[2]['weight'],'layer':ele[2]['layer']}
#             links_list.append(link_dict)

#         nodecnt=0
#         for inx, val in enumerate(py_data2):# remember to delete static data
#             nodes_list.append({'node': str(inx), 'name': val, 'saliency': layerSaliency[nodecnt]})
#             nodecnt+=1

#         data = reduce(run_function, [[], ] + nodes_list)
#         for ele in links_list:
#             valued_nodes.append(int(ele['source']))
#             valued_nodes.append(int(ele['target']))
#             tokenPool.add(int(ele['source']))
#             tokenPool.add(int(ele['target']))
#         nodeData=[]

#         valued_nodes=list(set(valued_nodes))
#         print(tokenPool)
#         # print(valued_nodes)
#         # tokenPool.add()
#         print((i,valued_nodes))
#         for vn in valued_nodes:
#             nodeData.append(data[vn])
#         node_link_data = {'nodes': nodeData, 'links': links_list}
#         all_layer_node_link.append({'maxLayer':i,
#         'threshold':threshold,
#         'node_link':node_link_data})
    
#     # else:
#     #     pass
        
#     # b=json.dumps({
#     #     'all_layer_node_link':all_layer_node_link,
#     #     'tokenPool':list(tokenPool)})
#     # fb=open('./all_tree.json')
#     # fb.write(b)
#     # fb.close()
#     return jsonify({
#         'all_layer_node_link':all_layer_node_link,
#         'tokenPool':list(tokenPool)
#     #    'node_link': node_link_data
#     #    'tokens': py_data2,
#     #    'valued_nodes':valued_nodes
#    })
    with open ('./all_tree.json') as f:
        jsonStr=json.load(f)
    return jsonify(jsonStr)


    



if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
