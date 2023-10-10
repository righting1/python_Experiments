def bouncing_ball(h, bounce, window):#h大于0 ,bounce大于0，小于1 ,window<h
    # your code
    if h<0:
        return -1
    if bounce<=0:
        return -1
    if bounce>=1:
        return -1
    if window>=h:
        return -1
    h=h*bounce
    ans=1
    while window<h:
        ans+=2
        h=h*bounce
    return ans