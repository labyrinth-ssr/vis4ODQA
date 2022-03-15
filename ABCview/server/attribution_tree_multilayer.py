from ctypes.wintypes import tagRECT
import numpy as np
import json
# import matplotlib.pyplot as plt
# import matplotlib as mpl
import copy


def attribution_tree(attr_file: str, tokens_file: str, example_index: int, threshold: int, layer: int):
    with open(attr_file) as fin:
        att_all = []
        for line in fin:
            att_all.append(json.loads(line))
        att_all = np.array(att_all).sum(1)
    proportion_all = copy.deepcopy(att_all)
    for i in range(len(proportion_all)):
        proportion_all[i] /= abs(proportion_all[i][1:, :].max())

    # adjust the threshold
    threshold = threshold*(layer+1)/12
    print(layer)
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

# 获得所有token对token的attr（到某一层的累计后，滤出>threshold的关系）。
# 问题：tree从左到右的每一对是attr的souce和target。source的实际attr>target对其attr之和。attr是attn根据最终预测结果的梯度加权，so，这个加权体现在source-target关系上，会更加突出target。
# tree可以对retriever和reader通用。都是同时放入question和document。
# 如何得出sentence attr:一句句子的重要程度与其长度无关，与其包含的重要token（高attr有关） 考虑以最重要的几个token的attr（设置阈值）之和？

    top_token_index = arg_res[0] if arg_res[0] != 0 else arg_res[1]
    attribution_tree('../output/att_attr_all/attr_zero_base_exp'+str(sentence_id)+'.json',
        '../output/tokens_and_pred_100.json',sentence_id,threshold,layer)