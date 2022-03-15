from flask import (
    Flask, app, json, jsonify,request
)
from flask_cors import CORS  
from functools import reduce
from attribution_tree_multilayer import attribution_tree
import numpy as np
from tree_height import fileTreeHeight,singleTreeHeight
from sentence_span import getSentenceSpan 
from que_freq import getQueSunburst
from head_importance import process_impo,process_layer
from queTreeToLink import queTreeToLink

all_layer_node_link=[]
list_tokenPool=[]
tokens=[]
que_sankey_data={}
impo_list=[]
que_tree_list=[]
ctxs=[]
ret={}
k=20

with open ('./generated_data/reader_results.json','r') as f_reader:
    reader_str=json.load(f_reader)
with open ('./generated_data/retriever_results.json','r') as f2:
    retriver_str=json.load(f2)

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/query_em_accu',methods=['GET'])
def query_em_accu():
    ret={'accu_em':[],'em_avg':int,'k_accu_avg':int}
    top_k_accu=[]
    ems=[]
    for ele in retriver_str:
        top_k_accu.append(ele['has_answer_num_in_top_20']/20)
        ems.append(1 if ele['top_20_has_answer'] else 0)
    ret['k_accu_avg']=sum(top_k_accu)/len(top_k_accu)
    ret['em_avg']=sum(ems)/len(ems)
    for parent in que_tree_list:
        if (not parent['name']==''):
            for child in parent['children']:
                sens=child['senId']
                link_em=sum([ems[id] for id in sens])/len(sens)
                link_accu=sum([top_k_accu[id] for id in sens])/len(sens)
                ret['accu_em'].append({'source':parent['name']+'_p','target':child['name']+'_c','em':link_em,'accu':link_accu})
    return jsonify(ret)

# @app.route('/query_ctx',methods=['POST','GET'])
# def query_ctx():
#     global reader_str,ctxs
#     if request.method=='POST':
#         # que_id=int(request.get_json()['que_id'])
#         que_id=0
#         ctx_all=reader_str[que_id]
#         ctxs=[ele]

@app.route('/query_que',methods=['GET'])
def query_que():
    global reader_str
    ques=[]
    # with open ('./generated_data/reader_results.json','r') as f:
    quelist=reader_str
    for i in range (0,len(quelist)):
        que_dict={'id':i,'que':quelist[i]['question']}
        ques.append(que_dict)
    return jsonify({'results':ques})

@app.route('/query_attn_head',methods=['GET'])
# 需要：len（link）个dict，（dict 组成的list）
# dict：{'layer_impo':[12],'head_impo':[12*12],'source':,'target':}
# 去除不需要的东西，如何获得senid？
def query_attn_head():
    global impo_list,que_tree_list
    with open ('./generated_data/summary/retriever_q_relevant.json','r') as f:
        str4d=np.array(json.load(f))
    str3d=np.sum(str4d,axis=1)/20
    sum=np.zeros([12,12])
    for parent in que_tree_list:
        if (not parent['name']==''):
            for child in parent['children']:
                senIds=child['senId']
                for i in senIds:
                    sum += np.array(str3d[i])
                sum /= len(senIds)
                suml=np.sum(sum,axis=1)
                impo_dict={'source':parent['name'],'target':child['name'],'head_impo':process_impo(sum.tolist()),
                'layer_impo':process_layer(suml.tolist())}
                impo_list.append(impo_dict)
    return jsonify(impo_list)

@app.route('/query_que_sunburst',methods=['GET', 'POST'])
def query_que_sunburst():
    global que_sankey_data,que_tree_list
    if request.method=='POST':
        post_data=request.get_json()
        threshold=int(post_data['threshold'])
        head=int(post_data['head'])
        layer=int(post_data['layer'])
        que_tree_list=getQueSunburst(threshold,head,layer)
        que_sankey_data=queTreeToLink(que_tree_list)
    else:
        pass
    return jsonify(que_sankey_data)

# @app.route('/query_attr_tree/<int:sentence_id>',methods=['GET', 'POST'])
# def query_attr_tree(sentence_id):
#     global all_layer_node_link, tokens,list_tokenPool
#     top_kth=0
#     if request.method=='POST':
#         all_layer_node_link=[]
#         post_data=request.get_json()
#         threshold=post_data['threshold']
#         # layer=post_data['layer']
#         tokenPool=set()
#         with open ('./generated_data/attr_vec/vec_end_'+str(sentence_id)+'.json','r') as f1:
#             saliency=json.load(f1)
#         with open('./generated_data/tokens/input_tokens for_question'+str(sentence_id)+'.json', 'r') as f2:
#             tokens = json.load(f2)[top_kth]
#         with open ('./generated_data/cutted_attr_mat/cutted_mat_start_'+str(sentence_id)+'.json') as f3:
#             all_attr=json.load(f3)
#         for i in range(0,12):
#             py_data=attribution_tree(all_attr,tokens,threshold,i,top_kth)
#             valued_nodes=[]
#             layerSaliency=saliency[i][top_kth]
#             nodes_list = []
#             links_list = []
#             def run_function(x, y): return x if y in x else x + [y]
#             for ele in py_data:
#                 tar_index = ele[0].split('+')[1]
#                 soc_index = ele[1].split('+')[1]
#                 link_dict = {'source':
#                             soc_index, 'target': tar_index, 'value': ele[2]['weight'],'layer':ele[2]['layer']}
#                 links_list.append(link_dict)
#             nodecnt=0
#             for inx, val in enumerate(tokens):# remember to delete static data
#                 nodes_list.append({'node': str(inx), 'name': val, 'saliency': layerSaliency[nodecnt]})
#                 nodecnt+=1
#             data = reduce(run_function, [[], ] + nodes_list)
#             for ele in links_list:
#                 valued_nodes.append(int(ele['source']))
#                 valued_nodes.append(int(ele['target']))
#                 tokenPool.add(int(ele['source']))
#                 tokenPool.add(int(ele['target']))
#             nodeData=[]
#             valued_nodes=list(set(valued_nodes))
#             # tokenPool.add()
#             for vn in valued_nodes:
#                 nodeData.append(data[vn])
#             node_link_data = {'nodes': nodeData, 'links': links_list}
#             all_layer_node_link.append({'maxLayer':i,
#             'threshold':threshold,
#             'node_link':node_link_data})
#         list_tokenPool=list(tokenPool)
#         list_tokenPool.sort()
#     else:
#         pass

#     return jsonify({
#         'all_layer_node_link':all_layer_node_link,
#         'tokenPool':list_tokenPool,
#         'tree_height':fileTreeHeight(all_layer_node_link),
#         'sentence_span':getSentenceSpan(tokens)
#    })
# attr_vec/vec_end_
# cutted_attr_mat/cutted_mat_start_'+str(sentence_id)
def one_tree(dir_name1:str,dir_name2:str, layer:int,threshold:int,top_kth:int,tokenPool:set,treeHeight:int,ctx_flag:bool,noneed_cls:bool,tokens)->dict:
    with open ('./generated_data/'+dir_name2+'.json','r') as f1:
        saliency=json.load(f1)
    with open ('./generated_data/'+dir_name1+'.json','r') as f3:
        all_attr=json.load(f3)
    print('layer:',layer)
    py_data=attribution_tree(all_attr,tokens,threshold,layer,top_kth,ctx_flag,noneed_cls)
    valued_nodes=[]
    if (not ctx_flag):
        layerSaliency=saliency[layer][top_kth]
    else: 
        layerSaliency=saliency[layer]
    nodes_list = []
    links_list = []
    def run_function(x, y): return x if y in x else x + [y]
    for ele in py_data:
        tar_index = ele[0].split('+')[1]
        soc_index = ele[1].split('+')[1]
        if(noneed_cls and (tar_index =='0' or soc_index=='0')):
            continue
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
    # tokenPool.add()
    for vn in valued_nodes:
        nodeData.append(data[vn])
    node_link_data = {'nodes': nodeData, 'links': links_list}
    treeHeight+=singleTreeHeight(node_link_data)
    print(treeHeight)
    return node_link_data
    

@app.route('/query_single_attr_tree/<int:sentence_id>',methods=['GET', 'POST'])
def query_attr_tree(sentence_id):
    global ret
    if request.method=='POST':
        ret={'q_node_link':{},'ctx_node_link':{},'reranker_node_link':{},'reader_node_link':{}, 'tree_height':{'q':0,'ctx':0,'reranker':0,'reader':0},'sentence_span':[],'token_pool':[]}
        top_kth=0
        tokenPool=set()
        post_data=request.get_json()
        threshold=post_data['threshold']
        layer=post_data['layer']
        with open('./generated_data/tokens/input_tokens for_question'+str(sentence_id)+'.json', 'r') as f2:
            tokens = json.load(f2)[top_kth]
        sep_save=0
        for i in range(0,len(tokens)):
            if(tokens[i]=='[SEP]'):
                sep_save=i
        q_tokens=tokens[:sep_save+1]
        ctx_tokens=['[CLS]']
        ctx_tokens.extend(tokens[sep_save+1:])
        ctx_tokens.append('[SEP]')

        ret['q_node_link']=one_tree('relevant_q/attr_mat/mat_relevant_'+str(sentence_id), 'relevant_q/attr_vec/vec_relevant_'+str(sentence_id),layer,threshold,top_kth,tokenPool,ret['tree_height']['q'],False,True,q_tokens)
        ret['tree_height']['q']=singleTreeHeight(ret['q_node_link'])
        ret['ctx_node_link']= one_tree('relevant_ctx/attr_mat/mat_relevant_'+str(sentence_id),'relevant_ctx/attr_vec/vec_relevant_'+str(sentence_id),layer,threshold,top_kth,tokenPool,ret['tree_height']['ctx'],True,True,ctx_tokens)
        ret['tree_height']['ctx']=singleTreeHeight(ret['ctx_node_link'])
        ret['reranker_node_link']= one_tree('rank/attr_mat/mat_rank_'+str(sentence_id), 'rank/attr_vec/vec_rank_'+str(sentence_id),layer,threshold,top_kth,tokenPool,ret['tree_height']['reranker'],False,False,tokens)
        ret['tree_height']['reranker']=singleTreeHeight(ret['reranker_node_link'])
        ret['reader_node_link']= one_tree('attr_mat/mat_start_'+str(sentence_id),'attr_vec/vec_end_'+str(sentence_id),layer,threshold,top_kth,tokenPool,ret['tree_height']['reader'],False,False,tokens)
        ret['tree_height']['reader']=singleTreeHeight(ret['reader_node_link'])
        list_tokenPool=list(tokenPool)
        list_tokenPool.sort()
        ret['token_pool']=list_tokenPool
        ret['sentence_span']=getSentenceSpan(tokens)
        # with open ('./tree_data.json','r') as f:
        #     ret=json.load(f)
    else:
        pass

    return jsonify(ret)

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0')