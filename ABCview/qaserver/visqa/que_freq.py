import json
from cv2 import threshold

from numpy import save, size
res=[]
with open("./reader_results.json",'r') as load_f:
     load_list = json.load(load_f)
    #  print(load_list)
for x in load_list:
    res.append(x["question"]) 
ret={'name':'root','children':[]}

threshold=50
# def dict_to_list(parDict):
#     for parDictKey in parDict:
#         chiDict=parDict[parDictKey][1]
#         temp=[]
#         if(not chiDict[list(chiDict.keys())[0]][1]):#孩子是否为叶节点
#             for chiDictKey in chiDict:
#                 chiDictVal=chiDict[chiDictKey]
#                 temp.append({'name':chiDictKey,'size':chiDictVal[0]})
#             parDict[parDictKey][1]=temp
#             return
#         else: dict_to_list(chiDict)
#         tempa=[]
#         chiDict2=parDict[parDictKey][1]
#         for chiDictKey2 in chiDict2:
#             chiDictVal2=chiDict2[chiDictKey2]
#             tempa.append({'name':chiDictKey2,'size':chiDictVal2[0]})
#         parDict[parDictKey][1]=tempa
# ,'senId':chiDictVal[2]
# {'aristotelian': [1, {}, [3605]],'a':1}
temp1={}
for i in range(0,len(res)):
    y=res[i].split(' ',4)
    if(temp1.__contains__(y[0])):
        temp1[y[0]][0]+=1
        temp1[y[0]][2].append(i)
    else:temp1[y[0]]=[1,{},[i]]
    temp2=temp1[y[0]][1]
    if(temp2.__contains__(y[1])):
        temp2[y[1]][0]+=1
        temp2[y[1]][2].append(i)
    else:temp2[y[1]]=[1,{},[i]]
    temp3=temp1[y[0]][1][y[1]][1]
    if(temp3.__contains__(y[2])):
        temp3[y[2]][0]+=1
        temp3[y[2]][2].append(i)
    else:temp3[y[2]]=[1,{},[i]]
    temp4=temp1[y[0]][1][y[1]][1][y[2]][1]
    if(temp4.__contains__(y[3])):
        temp4[y[3]][0]+=1
        temp4[y[3]][2].append(i)
    else:temp4[y[3]]=[1,{},[i]]

def cmpSize(ele):
    return ele['size']

def filter_threshold(ele):
    return ele['size']>threshold

save1=[]
for key,val in temp1.items():
    save2=[]
    for k2,v2 in val[1].items():
        save3=[]
        for k3,v3 in v2[1].items():
            save4=[]
            for k4,v4 in v3[1].items():
                save4.append({'name':k4,'size':v4[0],'senId':v4[2]})
                save4.sort(key=cmpSize,reverse=True)
                save4=list(filter(filter_threshold,save4))
            save3.append({'name':k3,'size':v3[0],'children':save4,'senId':v3[2]})
            save3.sort(key=cmpSize,reverse=True)
            save3=list(filter(filter_threshold,save3))
        save2.append({'name':k2,'size':v2[0],'children':save3,'senId':v2[2]})
        save2.sort(key=cmpSize,reverse=True)
        save2=list(filter(filter_threshold,save2))
    save1.append({'name':key,'size':val[0],'children':save2,'senId':val[2]})
    save1.sort(key=cmpSize,reverse=True)
    save1=list(filter(filter_threshold,save1))
temp1=save1

# print(temp1)
    # for z in sorted(temp1.items(), key = lambda kv:(kv[1], kv[0]),reverse=True):
    #     temp11=[]
    #     temp11.append({'name':z[0],'size':z[1]})
    # ret['children']=temp11

b = json.dumps(temp1)    
f2 = open('first_four_freq.json', 'w')
f2.write(b)
f2.close()