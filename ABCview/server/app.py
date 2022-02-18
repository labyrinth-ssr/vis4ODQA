from flask import (
    Flask, app, json, jsonify,request
)
from flask_cors import CORS  # 前后端分离跨域
from attn_process import attnProcess
from head_importance import process_impo
from functools import reduce
import re
import ndjson
from attribution_tree_multilayer import attribution_tree


FILENAME1 = './sentence_token_pred_100.json'
FILENAME2 = './tsne_100.json'
FILENAME3 = './tsne_sentence_100.json'
node_link_data={}
py_data2=[]
valued_nodes=[]

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})


@app.route('/query_all')
def query_all():
    with open(FILENAME1) as f:
        jsonStr = json.load(f)
        return jsonify(jsonStr)


@app.route('/query_tsne')
def query_tsne():
    with open(FILENAME2) as f:
        jsonStr = json.load(f)
        return jsonify(jsonStr)

@app.route('/query_sentence_tsne')
def query_sentence_tsne():
    with open(FILENAME3) as f:
        jsonStr = json.load(f)
        return jsonify(jsonStr)

@app.route("/query_attn_head/<int:sentence_id>")
def query_attn_head(sentence_id):
    with open('../output/att_attr_all/att_score_zero_base_exp'+str(sentence_id)+'.json') as load_f:
        py_data = ndjson.load(load_f)
    with open('../output/head_importance_attr.json', 'r') as load_f2:
        py_data2 = json.load(load_f2)
    with open('./tokens.json', 'r') as load_f3:
        py_data3 = json.load(load_f3)
        return jsonify({
            'importance': process_impo(py_data2),
        'detail': attnProcess(py_data),
        'tokens': py_data3
        })
@app.route("/query_attn_map/<int:sentence_id>")
def query_attn_map(sentence_id):
    with open('../output/att_attr_all/attr_zero_base_exp'+str(sentence_id)+'.json') as load_f:
        py_data = ndjson.load(load_f)
    return jsonify({
        'detail': attnProcess(py_data)
    })

@app.route('/query_attr_tree/<int:sentence_id>',methods=['GET', 'POST'])
def query_attr_tree(sentence_id):
    global node_link_data,py_data2,valued_nodes
    if request.method=='POST':
        valued_nodes=[]
        post_data=request.get_json()
        threshold=post_data['threshold']
        layer=post_data['layer']
        py_data= attribution_tree('../output/att_attr_all/attr_zero_base_exp'+str(sentence_id)+'.json','../output/tokens_and_pred_100.json',sentence_id,threshold,layer)
        with open("./tokens.json", 'r') as load_f2:
            py_data2 = json.load(load_f2)
        nodes_list = []
        links_list = []
        def run_function(x, y): return x if y in x else x + [y]

        for ele in py_data:
            tar_index = re.findall(r'\d+', ele[0])[0]
            soc_index = re.findall(r'\d+', ele[1])[0]
            link_dict = {'source':
                        soc_index, 'target': tar_index, 'value': 2}
            links_list.append(link_dict)

        for inx, val in enumerate(py_data2):# remember to delete static data
            nodes_list.append({'node': str(inx), 'name': val})

        data = reduce(run_function, [[], ] + nodes_list)
        for ele in links_list:
            valued_nodes.append(int(ele['source']))
            valued_nodes.append(int(ele['target']))

        valued_nodes=list(set(valued_nodes))
        node_link_data = {'nodes': data, 'links': links_list}

    else:
        pass

    return jsonify({
        'node_link': node_link_data,
        'tokens': py_data2,
        'valued_nodes':valued_nodes
    })


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')
