def createTreeFromEdges(edges):
    tree = {}
    for i in edges:
        v1, v2 = i
        if v1 in tree:
            tree[v1].append(v2)
        else:
            tree[v1] = [v2]
    return tree

def getTreeHeight (root:str,t:dict):
    if (not t.__contains__(root)):
        return 0
    maxsubHeight=0
    for i in t[root]:
        maxsubHeight=max(getTreeHeight(i,t),maxsubHeight)
    return (maxsubHeight+1)

def fileTreeHeight (all_node_link:dict)->list:
    # with open ('./all_tree.json','r') as load_f:
    #     load_dict=json.load(load_f)
    all_layer_height=[]
    for layer in all_node_link:
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
        all_layer_height.append(tree_height)
            # print(height)
    # 对每一层的树，放一个link表 n*2
    return all_layer_height