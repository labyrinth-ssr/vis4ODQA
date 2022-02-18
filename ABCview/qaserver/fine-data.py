import json
from tkinter.tix import Tree
tokenPool= [
    0, 
    65, 
    66, 
    67, 
    68, 
    69, 
    2, 
    7, 
    4, 
    9, 
    3, 
    89, 
    1, 
    105, 
    53, 
    57, 
    59, 
    60
  ]
tokenPool.sort()
print(tokenPool)

# 计算树高：所有的link，扫一遍target，set数组。然后再扫一遍source。
# 顺序扫link，对于target，若未出现，新增。若已出现，source++。（disjoint set）若原本归
# 1 2 3 4 5
# 4 5
# 如何做到？

class DSU:
    def __init__(self, elements:list[str]):
        self.root = {ele:ele for ele in elements}
        print (self.root)
        
    def find(self, k):
        if self.root[k] == k:
            return k
        self.root[k] = self.find(self.root[k])
        return self.root[k]
    
    def union(self, a, b):
        x = self.find(a)
        y = self.find(b)
        if x != y:
            self.root[y] = x
        return

def findMaxSet(M: list[list[str]],elements:list[str]) -> int:
    n = len(M)
    dsu = DSU(elements)
    for pair in M:
        dsu.union(pair[0],pair[1])
    ds_dict={ele:0 for ele in elements}
    for ele in elements:
        ds_dict[dsu.find(ele)]+=1
    ret=sorted(ds_dict.values(),reverse=True)
    print (ret)
    return ret

def createTreeFromEdges(edges):
    tree = {}
    for i in edges:
        v1, v2 = i
        if v1 in tree:
            tree[v1].append(v2)
        else:
            tree[v1] = [v2]

        # if v2 in tree:
        #     tree[v2].append(v1)
        # else:
        #     tree[v2] = [v1]

    return tree

def getTreeHeight (root:str,t:dict):
    if (not t.__contains__(root)):
        return 0
    maxsubHeight=0
    for i in t[root]:
        maxsubHeight=max(getTreeHeight(i,t),maxsubHeight)
    return (maxsubHeight+1)

with open ('./all_tree.json','r') as load_f:
    load_dict=json.load(load_f)
all_layer_link=load_dict['all_layer_node_link']
for layer in all_layer_link:
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
        # print(height)
# 对每一层的树，放一个link表 n*2
    print(tree_height)


