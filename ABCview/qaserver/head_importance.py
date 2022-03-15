def process_impo(py_data):
    headImportance=[]
    max_attn=0
    for i in range (0,12):
        for j in range (0,12):
            max_attn=max(max_attn,py_data[i][j])
            importanceDict={'layer':i,'head':j,'val':py_data[i][j] }
            headImportance.append(importanceDict)
    return (headImportance)
# print(headImportance)
def process_layer(data1d):
    layer_impo=[]
    max_attn=0
    for i in range (0,12):
        max_attn=max(max_attn,data1d[i])
        impo_dict={'layer':i,'val':data1d[i]}
        layer_impo.append(impo_dict)
    return (layer_impo)