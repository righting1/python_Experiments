def get_count(sentence):
    #pass
    ans=0
    for i in sentence:
        if i=='a'or i=='e'or i=='i' or i=='o' or i=='u' :
            ans+=1
    return ans
        