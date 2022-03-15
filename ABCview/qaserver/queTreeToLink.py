# 单纯以名字为唯一id
def queTreeToLink(tree_data:list)->dict:
    ret={'nodes':[],'links':[]}
    nodes=set()
    for parent in tree_data:
        if (not parent['name']==''):
            for child in parent['children']:
                ret['links'].append({'source':parent['name']+'_p','target':child['name']+'_c','value':len(child['senId'])})
                nodes.add(parent['name']+'_p')
                nodes.add(child['name']+'_c')
    for node in nodes:
        ret['nodes'].append({'node':node,'name':node.split('_',1)[0]})
    return ret
