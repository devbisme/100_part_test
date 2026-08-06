import sys,re
def toks(s):
    i=0;n=len(s)
    while i<n:
        c=s[i]
        if c in '()': yield c; i+=1
        elif c=='"':
            j=i+1;buf=[]
            while s[j]!='"':
                if s[j]=='\\': buf.append(s[j+1]);j+=2
                else: buf.append(s[j]);j+=1
            yield ('S',''.join(buf)); i=j+1
        elif c.isspace(): i+=1
        else:
            j=i
            while j<n and not s[j].isspace() and s[j] not in '()"': j+=1
            yield ('A',s[i:j]); i=j
def parse(s):
    st=[[]]
    for t in toks(s):
        if t=='(': st.append([])
        elif t==')': v=st.pop(); st[-1].append(v)
        else: st[-1].append(t[1])
    return st[0][0]
def find(n,tag): return [x for x in n if isinstance(x,list) and x and x[0]==tag]
tree=parse(open(sys.argv[1]).read())
for sym in find(tree,'symbol'):
    for sub in find(sym,'symbol'):
        m=re.search(r'_(\d+)_(\d+)$',sub[1]); u=m.group(1) if m else '?'
        for p in find(sub,'pin'):
            num=find(p,'number')[0][1]; nm=find(p,'name')[0][1]
            alts=[a[1] for a in find(p,'alternate')]
            print(f"{num}\t{nm}\t{p[1]}\t{p[2]}\tu{u}\t{';'.join(alts)}")
