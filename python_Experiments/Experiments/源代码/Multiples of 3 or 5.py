def duplicate_encode(word):
    #your code here
    return "".join(["(" if word.lower().count(x)==1 else ")" for x in word.lower()])
