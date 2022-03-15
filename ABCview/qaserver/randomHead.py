import numpy as np
import json
a=[]
for i in range (0,3610):
    a.append
a=np.random.random((3610,20,12,12))

with open ('./random_head.json','w') as f:
    json.dump(a.tolist(),f)

# question：top20累加？
# attn是