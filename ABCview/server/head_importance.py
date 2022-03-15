def process_impo(py_data):
    
    headImportance=[]
    cnt=0
    for val in py_data:
        importanceDict={'layer':cnt//12,'head':cnt%12,'val':val }
        headImportance.append(importanceDict)
        cnt+=1
    return (headImportance)
# print(headImportance)