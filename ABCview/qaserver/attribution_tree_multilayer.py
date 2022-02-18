import numpy as np
import json
import networkx as nx
# import matplotlib.pyplot as plt
# import matplotlib as mpl
import copy

def attribution_tree(attr_file: str, tokens_file: str, example_index: int, threshold: int, layer: int,top_kth:int):
    att_all=[]
    with open(attr_file,'r') as load_f:
        att_allk=json.load(load_f)
    for layId in att_allk:
        att_all.append(layId[top_kth])
    att_all=np.array(att_all)
    
    proportion_all = copy.deepcopy(att_all)
    for i in range(len(proportion_all)):
        proportion_all[i] /= abs(proportion_all[i][1:, :].max())

    # adjust the threshold
    # threshold = threshold*(layer+1)/12
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
    # if layer == 11:
    #     layer -= 1
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

    # token examples
    # tokens = ["[CLS]", "i", "don", "'", "t", "know", "um", "do", "you", "do", "a", "lot", "of", "camping", "[SEP]", "I", "know", "exactly", ".", "[SEP]"]
    # tokens = ["[CLS]", "The", "new", "rights", "are", "nice", "enough", "[SEP]", "Everyone", "really", "likes", "the", "newest", "benefits", "[SEP]"]
    # tokens = ["[CLS]", "so", "i", "have", "to", "find", "a", "way", "to", "supplement", "that", "[SEP]", "I", "need", "a", "way", "to", "add", "something", "extra", ".", "[SEP]"]
    with open(tokens_file) as fin:
        tokens_all_k = json.load(fin)
        tokens_all=tokens_all_k[top_kth]
    tokens = tokens_all

    for i in range(len(tokens)):
        tokens[i] = tokens[i]+'+'+ str(i)

    # fig1 = plt.figure(1,figsize=(30,22)) 
    # fig1.patch.set_facecolor('xkcd:white')

    G = nx.DiGraph()

    for token in tokens:
        G.add_node(token)

    for (i_token, j_token) in edges:
        G.add_edges_from([(tokens[i_token], tokens[j_token], {'weight': weight[i_token][j_token],'layer':layerId[i_token][j_token]})])

    fix_position = {tokens[i]: [i / len(tokens), height_list[i]] for i in range(len(tokens))}
    M = G.number_of_edges()
    pos = nx.spring_layout(G, pos=fix_position)
    edge_colors = range(2, M + 2)

    unused_node = list(nx.isolates(G))
    for node in unused_node:
        G.remove_node(node)

    # edge_alphas = []
    edges_list = list(G.edges.data())

    b = json.dumps(edges_list)
    f2 = open('edges_list.json', 'w')
    f2.write(b)
    f2.close()
    return edges_list

attribution_tree('./generated_data/attr_mat/mat_start_1.json','./generated_data/tokens/input_tokens for_question1.json',1,0.6,6,0)

