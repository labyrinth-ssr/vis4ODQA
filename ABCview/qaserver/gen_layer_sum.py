with open ('./generated_data/summary/'+sum_fname+'.json','r') as f:
            str4d=np.array(json.load(f))
        str3d=np.sum(str4d,axis=1)/20
        sum=np.zeros([12,12])
        for parent in que_tree_list:
            if (not parent['name']==''):
                for child in parent['children']:
                    senIds=child['senId']
                    for i in senIds:
                        sum += np.array(str3d[i])
                    sum /= len(senIds)
                    suml=np.sum(sum,axis=1)
                    impo_dict={'source':parent['name'],'target':child['name'],'head_impo':process_impo(sum.tolist()),
                    'layer_impo':process_layer(suml.tolist())}
                    impo_list.append(impo_dict)