import numpy as np
import networkx as nx
import copy

def attribution_tree(att_allk:list, tokens:list, threshold: int, layer: int,top_kth:int,is_cxt:bool,noneed_cls:bool):
    att_all=[]
    if (not is_cxt):
        for layId in att_allk:
            att_all.append(layId[top_kth])
        att_all=np.array(att_all)
    else: 
        att_all=np.array(att_allk)
    proportion_all = copy.deepcopy(att_all) 
    for i in range(len(proportion_all)):
        proportion_all[i] /= abs(proportion_all[i][1:, :].max())

    proportion_all *= (proportion_all > threshold).astype(int)

    seq_length = len(proportion_all[0])
    height_list = [0 for i in range(seq_length)]
    # -1: not appear  0: appear but not fixed  1: fixed   
    fixed_list = [-1 for i in range(seq_length)]
    edges = []

    # find the top node
    ig_remain = [0 for i in range(seq_length)]
    att_combine_layer = att_all.sum(0) / abs(att_all.sum(0).max())
    att_combine_layer *= (1 - np.identity(len(att_combine_layer))) * (att_combine_layer > 0)
    att_combine_layer[0] *= 0
    arg_res = np.argsort(att_combine_layer.sum(-1))[::-1]

    top_token_index = arg_res[0] if arg_res[0] != 0 else arg_res[1]
    height_list[top_token_index] = 11 / 12
    fixed_list[top_token_index] = 0
    if(noneed_cls):
        if layer == 11:
            layer -= 1
    weight = np.zeros(shape=(seq_length,seq_length))
    layerId = np.zeros(shape=(seq_length,seq_length))

    for i in range(seq_length):
        if i != top_token_index and proportion_all[layer][top_token_index][i] > threshold:
            fixed_list[i] = 0
            fixed_list[top_token_index] = 1
            edges.append((top_token_index, i))
            weight[top_token_index][i]=proportion_all[layer][top_token_index][i]
            layerId[top_token_index][i]=layer

    for layer_index in range(layer-1, -1, -1):
        for i_token in range(1, seq_length):
            for j_token in range(0, seq_length):
                if proportion_all[layer_index][i_token][j_token] < threshold or fixed_list[i_token] == -1:
                    continue
                if fixed_list[j_token] == 1:
                    continue
                if (i_token, j_token) in edges:
                    continue
                if fixed_list[i_token] == 0 and fixed_list[j_token] == 0:
                    continue
                if fixed_list[i_token] == 1 and fixed_list[j_token] == 0:
                    continue
                if fixed_list[i_token] == 0 and fixed_list[j_token] == -1:
                    fixed_list[i_token] = 1
                    fixed_list[j_token] = 0
                    height_list[j_token] = ((height_list[i_token]) * 12 - 1) / 12
                if fixed_list[i_token] == 1 and fixed_list[j_token] == -1:
                    fixed_list[j_token] = 0
                    height_list[j_token] = min(height_list)
                edges.append((i_token, j_token))
                weight[i_token][j_token]=proportion_all[layer_index][i_token][j_token]
                layerId[i_token][j_token]=layer_index

    tagged_tokens=[]
    for i in range(len(tokens)):
        tagged_tokens.append(tokens[i]+'+'+ str(i)) 

    G = nx.DiGraph()

    for token in tagged_tokens:
        G.add_node(token)

    for (i_token, j_token) in edges:
        print(tagged_tokens[i_token],tagged_tokens[j_token])

        G.add_edges_from([(tagged_tokens[i_token], tagged_tokens[j_token], {'weight': weight[i_token][j_token],'layer':layerId[i_token][j_token]})])
    M = G.number_of_edges()

    unused_node = list(nx.isolates(G))
    for node in unused_node:
        G.remove_node(node)

    edges_list = list(G.edges.data())

    return edges_list
