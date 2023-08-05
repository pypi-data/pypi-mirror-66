import elist.elist as elel
import edict.edict as eded

class Null():
    pass

null = Null()


class Orb(object):
    def __init__(self,ele):
        self.__dict__['__ctrl'] = {}
        self.__dict__['__ele'] = ele
    def __setitem__(self,k,v):
        self.__dict__['__ctrl'][k] = v
    def __getitem__(self,k):
        return(self.__dict__['__ctrl'][k])
    def __repr__(self):
        return(self.__dict__['__ctrl'].__repr__())



def get_children(jobj):
    if(isinstance(jobj,list)):
        children = elel.mapiv(jobj,lambda i,r:(i,r))
    elif(isinstance(jobj,dict)):
        children = eded.d2kvlist(jobj)
    elif(isinstance(jobj,tuple)):
        children = elel.mapiv(jobj,lambda i,r:(i,r))
    else:
        children = [(null,jobj)]
    return(children)


class Orb(object):
    def __init__(self,ele):
        self.__dict__['__ele'] = ele
        self.__dict__['__type'] = type(ele)
    def __setitem__(self,k,v):
        self.__dict__['__ctrl'][k] = v
    def __getitem__(self,k):
        return(self.__dict__['__ctrl'][k])
    def __repr__(self):
        return(self.__dict__['__ctrl'].__repr__())


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


def ele2orb(ele):
    rorb = Orb(ele)
    unhandled = [rorb]
    next_unhandled = []
    while(len(unhandled) >0):
        for i in range(len(unhandled)):
            orb = unhandled[i]
            ele = orb.__dict__['__ele']
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


