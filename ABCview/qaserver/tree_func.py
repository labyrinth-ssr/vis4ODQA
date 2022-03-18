import json
from attribution_tree_multilayer import attribution_tree
from functools import reduce

import numpy as np

def createTreeFromEdges(edges):
    tree = {}
    for i in edges:
        v1, v2 = i
        if v1 in tree:
            tree[v1].append(v2)
        else:
            tree[v1] = [v2]
    return tree

def getTreeHeight (root:str,t:dict):
    if (not t.__contains__(root)):
        return 0
    maxsubHeight=0
    for i in t[root]:
        maxsubHeight=max(getTreeHeight(i,t),maxsubHeight)
    return (maxsubHeight+1)

def fileTreeHeight (all_node_link:dict)->list:
    # with open ('./all_tree.json','r') as load_f:
    #     load_dict=json.load(load_f)
    all_layer_height=[]
    for layer in all_node_link:
        tree_height=0
        links=layer['node_link']['links']
        # nodes=layer['node_link']['nodes']
        # elements=[ele['node'] for ele in nodes]
        relations=[[ele['target'],ele['source']] for ele in links]
        my_tree=createTreeFromEdges(relations)
        tree_height=0 
        # print (my_tree)
        for root in my_tree:
            height=getTreeHeight(root,my_tree)
            tree_height=max(tree_height,height)
        all_layer_height.append(tree_height)
            # print(height)
    # 对每一层的树，放一个link表 n*2
    return all_layer_height

def singleTreeHeight (node_link:dict)->int:
    tree_height=0
    links=node_link['links']
    # nodes=layer['node_link']['nodes']
    # elements=[ele['node'] for ele in nodes]
    relations=[[ele['target'],ele['source']] for ele in links]
    my_tree=createTreeFromEdges(relations)
    # print (my_tree)
    for root in my_tree:
        height=getTreeHeight(root,my_tree)
        tree_height=max(tree_height,height)
    return tree_height

#ctx cls与q sep重叠，不跳过
def one_tree(node_begin_index:int, mat_dir:str,vec_dir:str, layer:int,threshold:int,top_kth:int,tokenPool:set,treeHeight:int,ctx_flag:bool,noneed_cls:bool,tokens)->dict:
    with open ('./generated_data/'+vec_dir+'.json','r') as f1:
        saliency=json.load(f1)
    with open ('./generated_data/'+mat_dir+'.json','r') as f3:
        all_attr=json.load(f3)
    print('layer:',layer)
    if(ctx_flag):
        for i in range (12):
            print ('length',len(all_attr),len(tokens))
            temp=(np.array(all_attr[i]))[:len(tokens),:len(tokens)]
            all_attr[i]=temp.tolist()
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
        tar_index = str(int(ele[0].split('+')[1])+node_begin_index)
        soc_index = str(int(ele[1].split('+')[1])+node_begin_index)
        cls_index=str(node_begin_index)
        if(noneed_cls and (tar_index ==cls_index or soc_index==cls_index)):
            continue
        link_dict = {'source':
                    soc_index, 'target': tar_index, 'value': ele[2]['weight'],'layer':ele[2]['layer']}
        links_list.append(link_dict)
    nodecnt=0
    for inx, val in enumerate(tokens):# remember to delete static data
        nodes_list.append({'node': str(inx+node_begin_index), 'name': val, 'saliency': layerSaliency[nodecnt]})
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
    print(data)
    for vn in valued_nodes:
        print(vn)
        nodeData.append(data[vn-node_begin_index])
    node_link_data = {'nodes': nodeData, 'links': links_list}
    treeHeight+=singleTreeHeight(node_link_data)
    print(treeHeight)
    return node_link_data