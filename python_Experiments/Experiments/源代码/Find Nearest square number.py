def nearest_sq(n):
    # pass
    x=int(n**0.5)
    if x*x==n:
        return n
    y=x+1
    xx=abs(x*x-n)
    yy=abs(y*y-n)
    if xx<=yy:
        return x*x
    else :
        return y*y

