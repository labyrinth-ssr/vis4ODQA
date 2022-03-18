def getSentenceSpan(tokens:list)-> list:
    ret=[]
    cnt=0
    for token in tokens :
        # if 
        ret.append(cnt)
        if (token=='.' or token=='[SEP]' or token==';' or token=='?'):
            cnt+=1
    return ret
# 还有选k,,,qnq