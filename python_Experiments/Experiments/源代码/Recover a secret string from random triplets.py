def recoverSecret(triplets):
    #'triplets is a list of triplets from the secrent string. Return the string.'
    rk=[]
    for i in range(len(triplets)):
        for j in range(len(triplets[i])):
            rk.append(triplets[i][j])
    rk=set(rk);
    rk=list(rk);
    while 1:
        cnt=0
        for i in range(len(triplets)):
            for j in range(len(triplets[i])-1):
                x=triplets[i][j]
                y=triplets[i][j+1]
                rk_x=rk.index(x)
                rk_y=rk.index(y)
                if rk_x>rk_y:
                    rk[rk_x]=y
                    rk[rk_y]=x
                    cnt+=1
        if cnt==0:
            break
    return ''.join(rk)