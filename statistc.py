#-*-coding:utf-8-*-
#AIC=2k - 2ln(L)
import numpy as np
def min_local_max(args):
    print("************************************")
    ori = np.poly1d(args)
    print("args:",args)
    f_deri = ori.deriv()
    print("一阶倒数:",f_deri)
    s_deri = f_deri.deriv()
    print("二阶导数：",s_deri)
    root = np.roots(f_deri)
    print("根:",root)
    #print("root",root)
    for i in root:
        if type(i)!=type(np.complex128(1)):
            print(type(s_deri(i)))
            if s_deri(i) < 0:
                print("二阶带入结果:", i, s_deri(i))
                return [i, ori(i)]
    return [None,None]


def AIC(args,x,y):
    from math import log
    """
    AIC=2k-ln(L)
    K是模型参数个数,L是模型似然函数
    :param args:参数个数
    :param x:
    :param y:
    :return:
    """
    func = np.poly1d(args)
    num = len(x)
    p = len(args)
    predict_y = func(x)
    real_y = y
    res_all = np.sum((predict_y-real_y) ** 2)
    test = num*log(res_all)
    #print(test)
    result = num*log(res_all)+2*(p + 1)-num*log(num)
    return result

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
    from math import log
    func = np.poly1d(args)
    num = len(x)
    p = len(args)
    predict_y = func(x)
    real_y = y
    res_all = np.sum((predict_y - real_y) ** 2)
    # print(test)
    result = num * log(res_all) + (p + 1)*log(num) - num * log(num)
    return result