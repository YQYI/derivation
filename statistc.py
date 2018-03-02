#-*-coding:utf-8-*-
#AIC=2k - 2ln(L)
import numpy as np
def computeLocalMax(args):
#def compute(args):
    ori = np.poly1d(args)
    der = ori.deriv()
    root = np.roots(der)
    validRoot = []
    for i in root:
        if isinstance(i, float):
            validRoot.append(i)

    # print("root:",root)
    result = ori(validRoot)
    print("value:", result)
    result = result.tolist()
    if result:
        i = result.index(max(result))
        return [validRoot[i], result[i]]
    else:
        return [-1, -1]

def AIC(args,x,y):
    pass

def r2(args,x,y):
    # r-squared
    p = np.poly1d(args)
    # fit values, and mean
    yhat = p(x)
    ybar = np.sum(y) / len(y)
    ssreg = np.sum((yhat - ybar) ** 2)
    sstot = np.sum((y - ybar) ** 2)
    rSqure = ssreg / sstot  # 准确率
    return rSqure

def BIC(args,x,y):
    pass