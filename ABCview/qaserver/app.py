from flask import (
    Flask, app, json, jsonify,request
)
from flask_cors import CORS  
from functools import reduce
from attribution_tree_multilayer import attribution_tree
from tree_height import fileTreeHeight
from sentence_span import getSentenceSpan 

all_layer_node_link=[]
list_tokenPool=[]
tokens=[]

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/query_attr_tree/<int:sentence_id>',methods=['GET', 'POST'])
def query_attr_tree(sentence_id):

    global all_layer_node_link, tokens,list_tokenPool

    top_kth=0
    

    if request.method=='POST':
        all_layer_node_link=[]
        post_data=request.get_json()
        threshold=post_data['threshold']
        print (threshold)
        # layer=post_data['layer']
        tokenPool=set()
        with open ('./generated_data/attr_vec/vec_end_'+str(sentence_id)+'.json','r') as f1:
            saliency=json.load(f1)
        with open('./generated_data/tokens/input_tokens for_question'+str(sentence_id)+'.json', 'r') as f2:
            tokens = json.load(f2)[top_kth]
        with open ('./generated_data/cutted_attr_mat/cutted_mat_start_'+str(sentence_id)+'.json') as f3:
            all_attr=json.load(f3)
        for i in range(0,12):
            py_data=attribution_tree(all_attr,tokens,threshold,i,top_kth)
            # print (tokens)
            valued_nodes=[]
            layerSaliency=saliency[i][top_kth]
            nodes_list = []
            links_list = []
            def run_function(x, y): return x if y in x else x + [y]

            for ele in py_data:
                tar_index = ele[0].split('+')[1]
                soc_index = ele[1].split('+')[1]
                link_dict = {'source':
                            soc_index, 'target': tar_index, 'value': ele[2]['weight'],'layer':ele[2]['layer']}
                links_list.append(link_dict)

            nodecnt=0
            for inx, val in enumerate(tokens):# remember to delete static data
                nodes_list.append({'node': str(inx), 'name': val, 'saliency': layerSaliency[nodecnt]})
                nodecnt+=1

            data = reduce(run_function, [[], ] + nodes_list)
            for ele in links_list:
                valued_nodes.append(int(ele['source']))
                valued_nodes.append(int(ele['target']))
                tokenPool.add(int(ele['source']))
                tokenPool.add(int(ele['target']))
            nodeData=[]

            valued_nodes=list(set(valued_nodes))
            # print(valued_nodes)
            # tokenPool.add()
            # print((i,valued_nodes))
            for vn in valued_nodes:
                nodeData.append(data[vn])
            node_link_data = {'nodes': nodeData, 'links': links_list}
            all_layer_node_link.append({'maxLayer':i,
            'threshold':threshold,
            'node_link':node_link_data})
        list_tokenPool=list(tokenPool)
        list_tokenPool.sort()
        
    else:
        pass

    return jsonify({
        'all_layer_node_link':all_layer_node_link,
        'tokenPool':list_tokenPool,
        'tree_height':fileTreeHeight(all_layer_node_link),
        'sentence_span':getSentenceSpan(tokens)
   })

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')