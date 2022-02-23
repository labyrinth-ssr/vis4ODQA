import json

start_index=0;end_index=3609;n_layer=12;n_k=20
for i in range (start_index,end_index+1):
    seq_len=[]
    with open ('./generated_data/attr_mat/mat_start_'+str(i)+'.json') as f:
        attr4d=json.load(f)# (layer,k,stc_length,sen_length)
    with open ('./generated_data/tokens/input_tokens for_question'+str(i)+'.json','r') as f3:
        tokens2d=json.load(f3)
        for seq in tokens2d:
            seq_len.append(len(seq))
    for layer_id in range(0,n_layer):
        for k_id in range(0,n_k):
            attr4d[layer_id][k_id]=attr4d[layer_id][k_id][:seq_len[k_id]]
            for token_id in range(0,seq_len[k_id]):
                attr4d[layer_id][k_id][token_id]=attr4d[layer_id][k_id][token_id][:seq_len[k_id]]
    with open ('./generated_data/cutted_attr_mat/cutted_mat_start_'+str(i)+'.json','w') as f2:
        json.dump(attr4d,f2)
