import json
def getQueSunburst(threshold,layer,head)->list:
    res=[]
    head_impo=[]
    with open('./random_head.json','r') as f:
        all_attn=json.load(f)
    for sen in all_attn:
        head_impo.append(sen[layer][head])
    with open("./reader_results.json",'r') as load_f:
        load_list = json.load(load_f)
        #  print(load_list)
    for x in load_list:
        res.append(x["question"]) 
    # ret={'name':'root','children':[]}
    # threshold=50
    temp1={}
    for i in range(0,len(res)):
        y=res[i].split(' ',2)
        if(temp1.__contains__(y[0])):
            temp1[y[0]][0]+=1
            temp1[y[0]][2].append(i)
        else:temp1[y[0]]=[1,{},[i]]
        temp2=temp1[y[0]][1]
        if(temp2.__contains__(y[1])):
            temp2[y[1]][0]+=1
            temp2[y[1]][2].append(i)
        else:temp2[y[1]]=[1,{},[i]]

    def cmpSize(ele):
        return ele['size']

    def filter_threshold(ele):
        return ele['size']>threshold
    def less_thre(ele):
        return ele['size']<threshold
    def assem_res(res):
        senId=[]
        for ele in res:
            senId+=ele['senId']
        return {'name':'','size':len(senId),'senId':senId,}
    save1=[]
    for key,val in temp1.items():
        save2=[]
        for k2,v2 in val[1].items():
            attn_sum2=0
            for id in v2[2]:
                attn_sum2+=head_impo[id]
            save2.append({'name':k2,'size':v2[0],'senId':v2[2],'val':attn_sum2/v2[0]})
        save2.sort(key=cmpSize,reverse=True)
        res2=list(filter(less_thre,save2))
        save2=list(filter(filter_threshold,save2))
        save2.append(assem_res(res2))
        attn_sum=0
        for id in val[2]:
            attn_sum+=head_impo[id]
        save1.append({'name':key,'size':val[0],'children':save2,'senId':val[2],'val':attn_sum/val[0]})
    save1.sort(key=cmpSize,reverse=True)
    res1=list(filter(less_thre,save1))
    save1=list(filter(filter_threshold,save1))
    save1.append(assem_res(res1))
    temp1=save1
    return temp1
