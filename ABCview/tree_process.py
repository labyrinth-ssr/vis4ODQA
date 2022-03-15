import json
from functools import reduce
import re

layer=6
threshold=0.4
valued_nodes=[]
top_kth=0
# threshold=post_data['threshold']
# py_data= attribution_tree('../output/att_attr_all/attr_zero_base_exp'+str(sentence_id)+'.json',
# '../output/tokens_and_pred_100.json',sentence_id,threshold,layer)

f=open('./edges_list.json','r')
f2=open('./vec_start_1.json','r')
py_data=json.loads(f.read())
saliency=json.loads(f2.read())
saliency=saliency[layer][top_kth]
with open("./input_tokens for_question1.json", 'r') as load_f2:
    py_data2 = json.load(load_f2)
    py_data2=py_data2[0]
nodes_list = []
links_list = []
def run_function(x, y): return x if y in x else x + [y]

for ele in py_data:
    print(ele[0].split('+'))
    
    tar_index = ele[0].split('+')[1]
    soc_index = ele[1].split('+')[1]
    link_dict = {'source':
                soc_index, 'target': tar_index, 'value': ele[2]['weight']}
    links_list.append(link_dict)

nodecnt=0
for inx, val in enumerate(py_data2):# remember to delete static data
    nodes_list.append({'node': str(inx), 'name': val, 'saliency': saliency[nodecnt]})
    nodecnt+=1

data = reduce(run_function, [[], ] + nodes_list)
for ele in links_list:
    valued_nodes.append(int(ele['source']))
    valued_nodes.append(int(ele['target']))

valued_nodes=list(set(valued_nodes))
node_link_data = {'nodes': data, 'links': links_list}

b=json.dumps({
    'node_link': node_link_data,
    'tokens': py_data2,
    'valued_nodes':valued_nodes,
})
f2=open('tree_data.json','w')
f2.write(b)
f2.close()
