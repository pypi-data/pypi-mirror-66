from lxml import etree
from nvhtml import engine


def split_an(an):
    for i in range(len(an)):
        ch = an[i]
        if(ch in "0123456789"):
            break
        else:
            pass
    if(i == (len(an) -1) and not(ch in "0123456789")):
        ran = an
        seqs= []
    else:
        ran = an[:i]
        seqs = an[i:].split('_')
        seqs = elel.mapv(seqs,int)
    return(ran,seqs)


def is_comment(ele):
    return(isinstance(ele,lxml.etree._Comment))


def is_comment_tag(tag):
    cond = isinstance(tag,str)
    if(not(cond)):
        if(tag.__name__ == 'Comment'):
            return(True)
        else:
            return(False)
    else:
        return(False)


def tag2an(tag):
    cond = is_comment_tag(tag)
    if(cond):
        return('Comment')
    else:
        return(tag.replace('-','_'))


def an2tag(an):
    return(an.replace('_','-'))



def group_children_by_tag_and_set(children,orb):
    st=set({})
    for i in range(len(children)):
        child = children[i]
        ele = child.__dict__['_ele']
        tag = ele.tag
        an = tag2an(tag)
        if(an in st):
            eles = orb.__dict__[an]
            eles.append(child)
        else:
            orb.__dict__[an] = [child]
            st.add(an)

class Orb(object):
    #singleton _dict = {} 自定义的有singleton效果
    # __dict__ 没有singleton 效果,并且不会触发__setattr__
    # 但是会触发 __getattribute__
    def __init__(self,ele):
        self.__dict__['_ele'] = ele
    def __repr__(self):
        s = engine.beautify(self.__dict__['_ele'])
        return(s)
    def __getattribute__(self,an):
        #*args 在这个函数里 无法 使用 会随结果一起返回
        if(an[0]=="_"):
            return(object.__getattribute__(self,an))
        else:
            an,seqs = split_an(an)
            arr = self.__dict__[an]
            if(len(seqs) == 0):
                return(arr)
            elif(len(seqs) == 1):
                return(arr[seqs[0]])
            else:
                return(elel.select_seqs(arr,seqs))
    def __getitem__(self,func):
        eles = func(self.__dict__['_ele'])
        return(eles)



def ele2orb(ele):
    rorb = Orb(ele)
    unhandled = [rorb]
    next_unhandled = []
    while(len(unhandled) >0):
        for i in range(len(unhandled)):
            orb = unhandled[i]
            ele = orb.__dict__['_ele']
            ele_children = ele.getchildren()
            children = elel.mapv(ele_children,Orb)
            if(len(children) == 0):
                setattr(orb,"",None)
            else:
                pass
            group_children_by_tag_and_set(children,orb)
            next_unhandled = next_unhandled + children
        unhandled = next_unhandled
        next_unhandled = []
    return(rorb)



def html2orb(html_txt):
    r = engine.s2root(html_txt)
    html = ele2orb(r)
    return(html)

def url2orb(url):
    r=requests.get(url)
    html_txt = r.text
    r = engine.s2root(html_txt)
    html = ele2orb(r)
    return(html)
