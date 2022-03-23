from flask import (
    Flask, app, json, jsonify,request
)
from flask_cors import CORS  
import numpy as np
from collections import Counter
import string
import regex as re
import copy
from functools import reduce

from tree_func import singleTreeHeight,one_tree,attribution_tree,fileTreeHeight
from sentence_span import getSentenceSpan 
from que_freq import getQueSunburst,queTreeToLink
from head_importance import process_impo,process_layer

all_layer_node_link=[]
list_tokenPool=[]
tokens=[]
que_sankey_data={}
impo_list=[]
que_tree_list=[]
ctxs=[]
ret={}
k=20
ques=[]
# sentence_id = 9
# top_k_accu=[]


with open ('./generated_data/reader_results.json','r') as f_reader:
    reader_str=json.load(f_reader)
with open ('./generated_data/retriever_results.json','r') as f2:
    retriver_str=json.load(f2)
with open ('./generated_data/summary/retriever_q_relevant.json','r') as f:
    str4d=np.array(json.load(f))

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

@app.route('/query_em_accu',methods=['GET'])
def query_em_accu():
    # global top_k_accu
    top_k_accu=[]
    ret={'accu_em':[],'em_avg':int,'k_accu_avg':int}
    ems=[]
    for ele in retriver_str:
        top_k_accu.append(ele['has_answer_num_in_top_20']/20)
        ems.append(1 if ele['top_20_has_answer'] else 0)
    ret['k_accu_avg']=sum(top_k_accu)/len(top_k_accu)
    ret['em_avg']=sum(ems)/len(ems)
    for parent in que_tree_list:
        if (not parent['name']==''):
            for child in parent['children']:
                sens=child['senId']
                link_em=sum([ems[id] for id in sens])/len(sens)
                link_accu=sum([top_k_accu[id] for id in sens])/len(sens)
                ret['accu_em'].append({'source':parent['name']+'_p','target':child['name']+'_c','em':link_em,'accu':link_accu})
    return jsonify(ret)

@app.route('/query_attn_head',methods=['GET'])
def query_attn_head():
    global impo_list,que_tree_list,str4d
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
    return jsonify(impo_list)

@app.route('/query_que_sunburst',methods=['GET', 'POST'])
def query_que_sunburst():
    global que_sankey_data,que_tree_list
    if request.method=='POST':
        post_data=request.get_json()
        threshold=int(post_data['threshold'])
        head=int(post_data['head'])
        layer=int(post_data['layer'])
        que_tree_list=getQueSunburst(threshold,head,layer,reader_str)
        que_sankey_data=queTreeToLink(que_tree_list)
    else:
        pass
    return jsonify(que_sankey_data)

@app.route('/query_que',methods=['GET','POST'])
def query_que():
    global reader_str,ques
    if request.method=='POST':
        ques=[]
        senIds=request.get_json()
        top_k_accu=[]
        quelist=reader_str
        for index in senIds:
            top_k_accu.append(retriver_str[index]['has_answer_num_in_top_20']/20)
            que_dict={'id':index,'que':quelist[index]['question'],'em':quelist[index]['em'],'k_accu':retriver_str[index]['has_answer_num_in_top_20']/20}
            ques.append(que_dict)
        # for ele in retriver_str:
        #     top_k_accu.append(ele['has_answer_num_in_top_20']/20)
        # with open ('./generated_data/reader_results.json','r') as f:
        # quelist=reader_str
        # for i in range (0,len(quelist)):
        #     que_dict={'id':i,'que':quelist[i]['question'],'em':quelist[i]['em'],'k_accu':top_k_accu[i]}
        #     ques.append(que_dict)
    else: pass
    return jsonify({'results':ques})

@app.route('/query_attr_tree',methods=['GET', 'POST'])
def query_attr_tree():
    global all_layer_node_link, tokens,list_tokenPool
    # top_kth=0
    if request.method=='POST':
        all_layer_node_link=[]
        post_data=request.get_json()
        threshold=post_data['threshold']
        top_kth = post_data['top_kth']
        que_id=post_data['que_id']
        model=post_data['model']
        attr_filename=''
        sal_filename=''
        with open('./generated_data/tokens/input_tokens for_question'+str(que_id)+'.json', 'r') as f2:
            tokens = json.load(f2)[top_kth]
        if (model=='que'):
            attr_filename='relevant_q/attr_mat/mat_relevant_'
            sal_filename='relevant_q/attr_vec/vec_relevant_'
            noneed_cls=True
            is_ctx=False
        elif (model=='ctx'):
            attr_filename='relevant_ctx/attr_mat/mat_relevant_'
            sal_filename='relevant_ctx/attr_vec/vec_relevant_'
            noneed_cls=True
            is_ctx=True
            que_id=que_id*20+top_kth #the file id,not the que id
        elif (model == 'reranker'):
            attr_filename='rank/attr_mat/mat_rank_'
            sal_filename='rank/attr_vec/vec_rank_'
            noneed_cls=False
            is_ctx=False
        elif (model == 'reader'):
            attr_filename='cutted_attr_mat/cutted_mat_start_'
            sal_filename='attr_vec/vec_end_'
            noneed_cls=True
            is_ctx=False
        # layer=post_data['layer']
        tokenPool=set()
        with open ('./generated_data/'+sal_filename+str(que_id)+'.json','r') as f1:
            saliency=json.load(f1)
        with open ('./generated_data/'+attr_filename+str(que_id)+'.json') as f3:
            all_attr=json.load(f3)
        if(is_ctx):
            for i in range (12):
                temp=(np.array(all_attr[i]))[:len(tokens),:len(tokens)]
                all_attr[i]=temp.tolist()
        for i in range(0,12):
            print('layer:',i)
            py_data=attribution_tree(all_attr,tokens,threshold,i,top_kth,is_ctx,noneed_cls)
            valued_nodes=[]
            if(is_ctx):
                layerSaliency=saliency[i]
            else:layerSaliency=saliency[i][top_kth]
            nodes_list = []
            links_list = []
            def run_function(x, y): return x if y in x else x + [y]
            for ele in py_data:
                tar_index = ele[0].split('+')[1]
                soc_index = ele[1].split('+')[1]
                link_dict = {'source':
                            soc_index, 'target': tar_index, 'value': ele[2]['weight'],'layer':ele[2]['layer']}
                links_list.append(link_dict)
            nodecnt=0
            for inx, val in enumerate(tokens):# remember to delete static data
                nodes_list.append({'node': str(inx), 'name': val, 'saliency': layerSaliency[nodecnt]})
                nodecnt+=1
            data = reduce(run_function, [[], ] + nodes_list)
            for ele in links_list:
                valued_nodes.append(int(ele['source']))
                valued_nodes.append(int(ele['target']))
                tokenPool.add(int(ele['source']))
                tokenPool.add(int(ele['target']))
            nodeData=[]
            valued_nodes=list(set(valued_nodes))
            # tokenPool.add()
            for vn in valued_nodes:
                nodeData.append(data[vn])
            node_link_data = {'nodes': nodeData, 'links': links_list}
            all_layer_node_link.append({'maxLayer':i,
            'threshold':threshold,
            'node_link':node_link_data})
        list_tokenPool=list(tokenPool)
        list_tokenPool.sort()
    else:
        pass

    return jsonify({
        'all_layer_node_link':all_layer_node_link,
        'tokenPool':list_tokenPool,
        'tree_height':fileTreeHeight(all_layer_node_link),
        'sentence_span':getSentenceSpan(tokens)
   })

@app.route('/query_single_attr_tree/<int:top_kth>',methods=['GET', 'POST'])
def query_single_attr_tree(top_kth):
    global ret,k
    if request.method=='POST':
        ret={'q_node_link':{},'ctx_node_link':{},'reranker_node_link':{},'reader_node_link':{}, 'tree_height':{'q':0,'ctx':0,'reranker':0,'reader':0},'sentence_span':[],'token_pool':[]}
        tokenPool=set()
        post_data=request.get_json()
        threshold=post_data['threshold']
        layer=post_data['layer']
        que_id=post_data['queId']
        with open('./generated_data/tokens/input_tokens for_question'+str(que_id)+'.json', 'r') as f2:
            tokens = json.load(f2)[top_kth]
        sep_save=0
        for i in range(0,len(tokens)):
            if(tokens[i]=='[SEP]'):
                sep_save=i
                break;
        q_tokens=tokens[:sep_save+1]
        ctx_tokens=['[CLS]']
        ctx_tokens.extend(tokens[sep_save+1:])
        ctx_tokens.append('[SEP]')

        ret['q_node_link']=one_tree(0,'relevant_q/attr_mat/mat_relevant_'+str(que_id), 'relevant_q/attr_vec/vec_relevant_'+str(que_id),layer,threshold['que'],top_kth,tokenPool,ret['tree_height']['q'],False,True,q_tokens)
        ret['tree_height']['q']=singleTreeHeight(ret['q_node_link'])
        ret['ctx_node_link']= one_tree(len(q_tokens)-1,'relevant_ctx/attr_mat/mat_relevant_'+str(que_id*20+top_kth),'relevant_ctx/attr_vec/vec_relevant_'+str(que_id*20+top_kth),layer,threshold['ctx'],top_kth,tokenPool,ret['tree_height']['ctx'],True,True,ctx_tokens)
        ret['tree_height']['ctx']=singleTreeHeight(ret['ctx_node_link'])
        ret['reranker_node_link']= one_tree(0,'rank/attr_mat/mat_rank_'+str(que_id), 'rank/attr_vec/vec_rank_'+str(que_id),layer,threshold['reranker'],top_kth,tokenPool,ret['tree_height']['reranker'],False,False,tokens)
        ret['tree_height']['reranker']=singleTreeHeight(ret['reranker_node_link'])
        ret['reader_node_link']= one_tree(0,'cutted_attr_mat/cutted_mat_start_'+str(que_id),'attr_vec/vec_end_'+str(que_id),layer,threshold['reader'],top_kth,tokenPool,ret['tree_height']['reader'],False,True,tokens)
        ret['tree_height']['reader']=singleTreeHeight(ret['reader_node_link'])
        list_tokenPool=list(tokenPool)
        list_tokenPool.sort()
        ret['token_pool']=list_tokenPool
        ret['sentence_span']=getSentenceSpan(tokens)
        # with open ('./tree_data.json','r') as f:
        #     ret=json.load(f)
        # ret=[]
    else:
        pass

    return jsonify(ret)


def exact_match_score(prediction, ground_truth):
    return _normalize_answer(prediction) == _normalize_answer(ground_truth)


def _normalize_answer(s):
    def remove_articles(text):
        return re.sub(r"\b(a|an|the)\b", " ", text)

    def white_space_fix(text):
        return " ".join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return "".join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_articles(remove_punc(lower(s))))


def summary_for_barchart(whole_wc, barchart_thre):
    q_summary = [token[0] for q in whole_wc for token in q if token[2] == 0]
    ctx_summary = [token[0] for q in whole_wc for token in q if token[2] > 0]
    # print(q_summary)
    # print(ctx_summary)
    q_dict = dict(Counter(q_summary))
    ctx_dict = dict(Counter(ctx_summary))
    keys_list = list(set(list(q_dict.keys()) + list(ctx_dict.keys())))
    summary_list = []
    only_q_summary = []
    only_ctx_summary = []
    both_summary = []
    for key in keys_list:
        q_value = 0 if key not in list(q_dict.keys()) else q_dict[key]
        ctx_value = 0 if key not in list(ctx_dict.keys()) else ctx_dict[key]
        if q_value > 0 and ctx_value == 0:
            only_q_summary.append([key, 1, q_value, 0])
        if ctx_value > 0 and q_value == 0:
            only_ctx_summary.append([key, 2, 0, ctx_value])
        if q_value > 0 and ctx_value > 0:
            both_summary.append([key, 0, q_value, ctx_value])
    only_q_summary = sorted(only_q_summary, key=lambda item: item[2], reverse=True)
    only_ctx_summary = sorted(only_ctx_summary, key=lambda item: item[3], reverse=True)
    both_summary = sorted(both_summary, key=lambda item: item[2] + item[3], reverse=True)
    # print(only_q_summary)
    # print(only_ctx_summary)
    # print(both_summary)
    only_q_summary = [x for x in only_q_summary if x[2] > barchart_thre]
    only_ctx_summary = [x for x in only_ctx_summary if x[3] > barchart_thre]
    both_summary = [x for x in both_summary if x[2] + x[3] > barchart_thre]
    return both_summary + only_q_summary + only_ctx_summary
    # print(list(ctx_dict.keys()))
    # keys_list = list({q_dict, ctx_dict}.keys())
    # print(keys_list)

    # q_list_unordered = list(dict(Counter(q_summary)).items())
    # q_list_ordered = sorted(q_list_unordered, key=lambda item: item[1], reverse=True)
    # ctx_list_unordered = list(dict(Counter(ctx_summary)).items())
    # ctx_list_ordered = sorted(ctx_list_unordered, key=lambda item: item[1], reverse=True)
    # return q_list_ordered, ctx_list_ordered


@app.route('/query_word_cloud/<int:sentence_id>', methods=['GET', 'POST'])
def query_word_cloud(sentence_id):
    if request.method == "POST":
        postdata = request.get_json()
        que_sal_thre = postdata['que_sal_thre']
        barchart_thre = postdata['barchart_thre']
    global q_whole, ctx_whole, rank_whole, span_whole, retriever_whole, q_select, ctx_select, retriever_select, rank_select, span_select
    with open('./generated_data/relevant_q/attr_whole/relevant_saliency_per_q_' + str(sentence_id) + '.json',
              'r') as f1:
        q_whole_saliency = json.load(f1)
    with open('./generated_data/relevant_ctx/attr_whole/relevant_saliency_per_q_' + str(sentence_id) + '.json',
              'r') as f2:
        ctx_whole_saliency = json.load(f2)
    with open('./generated_data/rank/attr_whole/rank_saliency_per_q_' + str(sentence_id) + '.json', 'r') as frank:
        rank_whole_saliency = json.load(frank)
    with open('./generated_data/span/attr_whole/span_saliency_per_q_' + str(sentence_id) + '.json', 'r') as fread:
        span_whole_saliency = json.load(fread)
    with open('./generated_data/tokens/input_tokens for_question' + str(sentence_id) + '.json', 'r') as f3:
        all_tokens = json.load(f3)
    with open('./generated_data/reader_results(present_each_psg).json') as f4:
        reader_results = json.load(f4)[sentence_id]
    with open('./generated_data/retriever_results.json') as f5:
        retriever_results = json.load(f5)[sentence_id]

    q_whole_wc = []
    ctx_whole_wc = []
    rank_whole_wc = []
    span_whole_wc = []
    retriever_whole_wc = []
    # q_whole_wc[i]: [('[cls]', 0.1), ..., ('[sep]', 0.1)]
    # ctx_whole_wc[i]: [('[cls]', 0.1), ..., ('[sep]', 0.1)]
    # TODO:
    # span_whole_wc[i]: [('[cls]', 0.1), ..., ('[sep]', 0.1)]
    for tokens_in_each_pair, q_in_each_pair, ctx_in_each_pair, rank_in_each_pair, span_in_each_pair \
            in zip(all_tokens, q_whole_saliency, ctx_whole_saliency, rank_whole_saliency, span_whole_saliency):
        # TODO:编码re-ranker/reader
        token_id_list = list(range(len(tokens_in_each_pair)))
        rank_whole_wc.append(list(zip(tokens_in_each_pair, rank_in_each_pair, getSentenceSpan(tokens_in_each_pair), token_id_list)))
        span_whole_wc.append(list(zip(tokens_in_each_pair, span_in_each_pair, getSentenceSpan(tokens_in_each_pair), token_id_list)))
        # TODO:编码retriever
        sep_index = tokens_in_each_pair.index("[SEP]")
        # question就一句话，不需要标记sentence idx，ctx需要；但是为了和树中的sentence idx一致，在前端处理时直接从title对应的颜色开始编码
        # FIXME: /10??
        tokens_in_each_pair.append("[SEP]")
        retriever_token_id = list(range(len(tokens_in_each_pair) + 1))
        q_id_list = retriever_token_id[:sep_index + 1]
        ctx_id_list = retriever_token_id[sep_index + 1:]
        q_in_each_pair_zip = np.array(q_in_each_pair[:sep_index + 1]) / 10
        q_in_each_pair_zip = q_in_each_pair_zip.tolist()
        # FIXME：否则用下面的
        # q_whole_wc.append(list(zip(tokens_in_each_pair[:sep_index + 1], q_in_each_pair[:sep_index + 1])))
        q_whole_wc.append(list(zip(tokens_in_each_pair[:sep_index + 1], q_in_each_pair_zip,
                                   getSentenceSpan(tokens_in_each_pair[:sep_index + 1]), q_id_list)))
        tokens_in_each_pair[sep_index] = "[CLS]"
        ctx_len = len(tokens_in_each_pair) - sep_index
        ctx_whole_wc.append(list(zip(tokens_in_each_pair[sep_index:], ctx_in_each_pair[:ctx_len],
                                     [i + 1 for i in getSentenceSpan(tokens_in_each_pair[sep_index:])], ctx_id_list)))
        # TODO: retriever整体
        tokens_in_each_pair[sep_index] = "[SEP]"

        whole_sentence_span = getSentenceSpan(tokens_in_each_pair)
        retriever_whole_wc.append(list(zip(tokens_in_each_pair[:sep_index+1] + ['[CLS]'] + tokens_in_each_pair[sep_index+1:],
                                           q_in_each_pair_zip + ctx_in_each_pair[:ctx_len],
                                           whole_sentence_span[:sep_index] + [1] + whole_sentence_span[sep_index:],
                                           retriever_token_id)))
    # print(q_whole_wc[4])
    # print(ctx_whole_wc[5])

    # TODO: 对re-ranker与reader的结果进行重排序
    gold_answers = reader_results['gold_answers']
    span_predictions = reader_results['predictions']
    em_result = []
    final_prediction = []
    for prediction in span_predictions:
        if prediction['prediction']['passage_idx'] >= 10:
            continue
        final_prediction.append(prediction['prediction']['text'])
        em_hit = max([exact_match_score(prediction['prediction']['text'], ga) for ga in gold_answers])
        em_result.append(em_hit)

    # print(em_result)
    order_result = [prediction['prediction']['passage_idx'] for prediction in
                    reader_results['predictions'] if prediction['prediction']['passage_idx'] < 10]
    has_answer_list = [ctx['has_answer'] for ctx in retriever_results['ctxs'][:10]]
    # print(has_answer_list)
    rank_whole_wc = [x for i, x in sorted(zip(order_result, rank_whole_wc[:10]))]
    span_whole_wc = [x for i, x in sorted(zip(order_result, span_whole_wc[:10]))]
    q_whole = copy.copy(q_whole_wc)
    ctx_whole = copy.copy(ctx_whole_wc)
    rank_whole = copy.copy(rank_whole_wc)
    span_whole = copy.copy(span_whole_wc)
    retriever_whole = copy.copy(retriever_whole_wc)
    q_select = copy.copy(q_whole_wc)
    ctx_select = copy.copy(ctx_whole_wc)
    rank_select = copy.copy(rank_whole_wc)
    span_select = copy.copy(span_whole_wc)
    retriever_select = copy.copy(retriever_whole_wc)

    q_saliency_threshold = que_sal_thre
    ctx_saliency_threshold = que_sal_thre
    retriever_saliency_threshold = que_sal_thre
    rank_saliency_threshold = que_sal_thre
    span_saliency_threshold = que_sal_thre
    for i, q in enumerate(q_whole_wc):
        q_whole_wc[i] = list(filter(lambda x: x[1] >= q_saliency_threshold, [token for token in q]))
        q_select[i] = [token[3] for token in q_whole_wc[i]]
    for i, ctx in enumerate(ctx_whole_wc):
        ctx_whole_wc[i] = list(filter(lambda x: x[1] >= ctx_saliency_threshold, [token for token in ctx]))
        ctx_select[i] = [token[3] for token in ctx_whole_wc[i]]
    for i, q_ctx in enumerate(rank_whole_wc):
        rank_whole_wc[i] = list(filter(lambda x: x[1] >= rank_saliency_threshold, [token for token in q_ctx]))
        rank_select[i] = [token[3] for token in rank_whole_wc[i]]
    for i, q_ctx in enumerate(span_whole_wc):
        span_whole_wc[i] = list(filter(lambda x: x[1] >= span_saliency_threshold, [token for token in q_ctx]))
        span_select[i] = [token[3] for token in span_whole_wc[i]]
    for i, q_ctx in enumerate(retriever_whole_wc):
        retriever_whole_wc[i] = list(filter(lambda x: x[1] >= retriever_saliency_threshold, [token for token in q_ctx]))
        retriever_select[i] = [token[3] for token in retriever_whole_wc[i]]
    # TODO: sentence_span to encode color
    # print(ctx_whole_wc[7])
    # for q in rank_whole_wc:
    #     b = sorted(q, key=lambda token: token[1], reverse=True)
    #     print(b)
    # for q in span_whole_wc:
    #     b = sorted(q, key=lambda token: token[1], reverse=True)
    #     print(b)

    # retriever_q_summary, _ = summary_for_barchart(q_whole_wc[:10])
    # _, retriever_ctx_summary = summary_for_barchart(ctx_whole_wc[:10])
    retriever_summary = summary_for_barchart(retriever_whole_wc[:10], barchart_thre)
    rank_summary = summary_for_barchart(rank_whole_wc[:10], barchart_thre)
    span_summary = summary_for_barchart(span_whole_wc[:10], barchart_thre)

    # print(retriever_summary)
    # print(rank_summary)
    # print(span_summary)
    # print(final_prediction)
    return jsonify({
        'q_whole_saliency': q_whole_wc[:10],
        'ctx_whole_saliency': ctx_whole_wc[:10],
        'rank_whole_saliency': rank_whole_wc[:10],
        'span_whole_saliency': span_whole_wc[:10],
        'order_result': order_result,
        'em_result': em_result,
        'has_answer_list': has_answer_list,
        'final_prediction': final_prediction,
        'gold_answer': gold_answers,
        # 'q_summary': q_summary,
        # 'ctx_summary': ctx_summary,
        # 'rank_summary': rank_summary,
        # 'span_summary': span_summary
        'retriever_summary': retriever_summary,
        'rank_summary': rank_summary,
        'span_summary': span_summary
    })


@app.route('/query_context_view/', methods=['GET', 'POST'])
def query_context_view():
    if request.method == "POST":
        postdata = request.get_json()
        ctx_id = postdata['ctx_id']
        stage_id = postdata['stage_id']
        if stage_id == 0:
            ret = {'tokens': retriever_whole[ctx_id], 'select': retriever_select[ctx_id]}
        elif stage_id == 1:
            ret = {'tokens': rank_whole[ctx_id], 'select': rank_select[ctx_id]}
        elif stage_id == 2:
            ret = {'tokens': span_whole[ctx_id], 'select': span_select[ctx_id]}
        else:
            raise
    else:
        pass
    # print(ret)
    return ret

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8000)