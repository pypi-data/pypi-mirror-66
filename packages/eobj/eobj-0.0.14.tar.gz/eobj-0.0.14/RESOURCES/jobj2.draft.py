import elist.elist as elel


class Null():
    def __repr__(self):
        return('null')

null = Null()


class Undefined():
    def __repr__(self):
        return('undefined')

undefined = Undefined()


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



def try_json_parse(s):
    try:
        j = json.loads(s)
    except:
        return(s)
    else:
        return(j)


def an2k(an):
    if(an[-1] == '_'):
        return(an[1:-1])
    else:
        return(an)


class Jobj(object):
    def __init__(self,ele,root=False):
        object.__setattr__(self,' ',null)
        self.__dict__['__ele'] = ele
        if(root):
            self.__dict__['__tag'] = 'root'
            self.__dict__['__parent'] = null
        else:
            self.__dict__['__tag'] = undefined
            self.__dict__['__parent'] = undefined
    def __repr__(self):
        return(self.__dict__['__ele'].__repr__())
    def __getattribute__(self,an):
        if(an[0]=="_"):
            return(object.__getattribute__(self,an))
        else:
            an,seqs = split_an(an)
            arr = self.__dict__[an]
            if(len(seqs) == 0):
                return(arr)
            elif(len(seqs) == 1):
                return(arr.__dict__[seqs[0]])
            else:
                return(list(eded.sub_algo(o.arr.__dict__,seqs).values()))

    def __delattr__(self,an):
        if(an[:2]=="__"):
            #和数据关联的控制数据
            raise(AttributeError('del ctrl attribute is not permited!!!'))
        elif(an[0]=="_"):
            #自定义控制数据，不和数据关联
            object.__delattr__(self,an)
        else:
            an,seqs = split_an(an)
            if(len(seqs) == 0):
                object.__delattr__(self,an)
                del self.__dict__['__ele'][an]
            elif(len(seqs) == 1):
                del self.__dict__[an].__dict__[seqs[0]]
                del self.__dict__['__ele'][an][seqs[0]]
            else:
                for seq in seqs:
                    del self.__dict__[an].__dict__[seq]
                    del self.__dict__['__ele'][an][seq]
    def __getitem__(self,k):
        return(self.__dict__[k])
    def __delitem__(self,k):
        del self.__dict__[k]
        del self.__dict__['__ele'][k]
    #def __setattr__(self,an,*args)
    #暂缓实现 要把 *args 变成 Jobj
    #def __setitem__
    #dumps


def _lele2chjobj(i,chele,ele):
    child = Jobj(chele)
    child.__dict__['__parent'] = ele
    child.__dict__['__tag'] = i
    return(child)

def _dele2chjobj(i,item,ele):
    chele = item[1]
    child = Jobj(chele)
    child.__dict__['__parent'] = ele
    child.__dict__['__tag'] = item[0]
    return(child)


def get_children(jobj):
    ele = jobj.__ele
    if(isinstance(ele,list)):
        children = elel.mapiv(ele,lambda i,chele:_lele2chjobj(i,chele,ele))
    elif(isinstance(ele,dict)):
        items = list(ele.items())
        children = elel.mapiv(items,lambda i,item:_dele2chjobj(i,item,ele))
    elif(isinstance(ele,tuple)):
        children = elel.mapiv(ele,lambda i,chele:_lele2chjobj(i,chele,ele))
    else:
        children =[]
    return(children)

def group_children_by_tag_and_set(children,jo):
    for i in range(len(children)):
        child = children[i]
        chele = child.__dict__['__ele']
        tag = child.__dict__['__tag']
        if(isinstance(jo.__dict__['__ele'],list)):
            jo.__dict__[tag] = child
        elif(isinstance(jo.__dict__['__ele'],tuple)):
            jo.__dict__[tag] = child
        elif(isinstance(jo.__dict__['__ele'],dict)):
            jo.__dict__[tag] = child
        else:
            pass


def ele2jobj(ele):
    rjobj = Jobj(ele,root=True)
    unhandled = [rjobj]
    next_unhandled = []
    while(len(unhandled) >0):
        for i in range(len(unhandled)):
            jo = unhandled[i]
            children = get_children(jo)
            group_children_by_tag_and_set(children,jo)
            next_unhandled = next_unhandled + children
        unhandled = next_unhandled
        next_unhandled = []
    return(rjobj)


