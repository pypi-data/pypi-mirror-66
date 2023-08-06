# coding:utf-8
import random
import re
import time


def replace_var_in_dict(strcvar,val):
    '''
    【功能】使用字典类型变量val中的value替换字符串strcvar中的${val.key}
    【参数】strcvar:字符串，包含需要被替换的字符串
            val：字典类型，只包含一个键值对，用于替换strcvar中部分字符串的字符串
    【返回】替换后的字符串
    '''
    val = dict(val)
    for k in val:
        strcvar = str(strcvar).replace('${'+ k +'}',str(dict(val)[k]))
    print('strcvar=%s'% strcvar)
    strcvar = eval(strcvar)
    return strcvar

def replace_var_in_str(strcvar,val):
    '''
    【功能】使用字典类型变量val中的value替换字符串strcvar中的${val.key}
    【参数】strcvar:字符串，包含需要被替换的字符串
            val：字典类型，只包含一个键值对，用于替换strcvar中部分字符串的字符串
    【返回】替换后的字符串
    '''
    for k in val:
        strcvar = str(strcvar).replace('${'+ k +'}',str(dict(val)[k]))
    print('strcvar=%s'% strcvar)
    return strcvar

def get_random_no_from_one(length):
    '''
    【功能】获取指定长度的随机数字
    【参数】length:随机数长度
    【返回】生成的随机数的字符串
    '''
    randomInt = random.randint(1,int(length))
    randomStr = str(randomInt).zfill(len(str(length)))
    print('randomStr=%s'% randomStr)
    return randomStr

def get_random_int_with_pre(pre,length):
    '''
    【功能】获取带前缀的指定长度的随机数字
    【参数】length:随机数长度
            pre:随机数前缀
    【返回】生成的随机数的字符串：前缀+随机数
    '''
    maxnum = 1
    for i in range(1,length):
        maxnum = maxnum * 10
    print('maxnum=%s'% maxnum)
    randomInt = random.randint(1,int(maxnum))
    randomStr = str(randomInt).zfill(len(str(maxnum)))
    print('randomStr=%s'% randomStr)
    return pre+randomStr

def replace_random_int_with_pre_in_str(originstr,pre):
    '''
    【功能】使用随机数表达式获得的随机数替换字符串中的随机数表达式
    【参数】originstr:原始字符串
            pre:随机数前缀
            ranexpstr:随机数表达式  __RN4 表示1至1000之内的随机正数
    【返回】替换后的字符串
    '''
    lst = re.findall(r'\{__RN(\d+)\}',str(originstr))
    neslst = lst.copy()
    for i in range(len(neslst)):
        # lst[i] = time.strftime("%Y%m%d", time.localtime())+lst[i]
        neslst[i] = get_random_int_with_pre(pre,int(lst[i]))
    print('neslst=%s'% neslst)
    dct = {}
    for j in range(len(lst)):
        dct[lst[j]] = neslst[j]
    print('dct=%s'% dct)
    newstr = originstr
    for key in dct:
        newstr = str(newstr).replace('{__RN'+key+'}',dct[key])
    print('newstr=%s'% newstr)
    return newstr
###===========================================================================================
if __name__=='__main__':
    str1 = 'adfas{__RN5}adsf{__RN5}asf{__RN4}'
    replace_random_int_with_pre_in_str(str1,'20200207')
    # print(get_random_int_with_pre('20200207',5))
    # str1='adfas{__RN5}adsfasf{__RN5}'
    # lt = re.findall(r'\{__RN(\d+)\}',str1)
    # print(lt)
    print(time.strftime("%Y%m%d", time.localtime()))