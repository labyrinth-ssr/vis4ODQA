import json
def getSentenceSpan(tokens:list)-> list:
    ret=[]
    cnt=0
    for token in tokens :
        # if 
        ret.append(cnt)
        if (token=='.' or token=='[SEP]' or token==';' or token=='?'):
            cnt+=1
    return ret

with open ('./generated_data/tokens/input_tokens for_question1.json') as fin:
    jsonStr=json.load(fin)
    getSentenceSpan(jsonStr[0])

# 还有选k,,,qnq