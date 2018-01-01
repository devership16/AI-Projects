# import time
####################################################### Utility Functions

def copy(varList):
    return [line[:] for line in varList]

def findarguments(query):
    return filter(lambda item: type(item) is list, query)

def findPredicate(query):
    return filter(lambda item: type(item) is str and item is not '~' and  item is not '|' , query) 

def isValid(queryPredicate,kbPredicates):
    return len(filter(lambda predicate: queryPredicate[0] in predicate,kbPredicates))>0

def isComplement(predx,predy):
    if '~' in predx[0]:
        predx[0]=predx[0][1:]
            
    else: 
        predx[0]='~'+predx[0]
    
    return (predx[0]==predy[0] and len(predx[1])==len(predy[1]))

def stringParseToTokens(query):
    query = '(' + query + ')'
    query = query.replace(',', ' ')
    query = query.replace('|', '')
    query = query.replace('(', ' ( ')
    query = query.replace(')', ' ) ')
    
    elements = query.split()

    return element_parseToList(elements)

def isVar(argument):
    if argument[0].islower():
        return True
    return False

def isFactKB(sentence):
    predicates=split_predicate(sentence)
    for predicate in predicates:
        print predicate[1]
        for i in xrange(len(predicate[1])):
            if predicate[1][i].islower():
                return False
    return True

def element_parseToList(elements):
    element = elements.pop(0)
    
    if element == '(':
        parsedquery = []
        while elements[0] != ')':
            parsedquery.append(element_parseToList(elements))
        elements.pop(0)
        return parsedquery
    else:
        return element
             
def split_predicate(predicate):
    return [predicate[i:i+2] for i in range(0, len(predicate), 2)]

def combine_predicate(predicate):
    result=[]
    for x in predicate:
        result.append(x[0])
        result.append(x[1])
    return result

def complementQuery(query):
    if '~' in query[0]:
        return query[0][1:]
    else: 
        return'~'+query[0]

def findComplement(query,parsedKB):
    pos=[]
    for i,predicate in enumerate(parsedKB):
        if query in predicate:
            pos.append(i)
    return pos

def findComplement_Sentence(sentence,parsedKB):
    split_sentence=split_predicate(sentence)
    max_pos=[]
    for predicate in split_sentence:
        predicate[0]=complementQuery(predicate)
        pos=findComplement(predicate[0],parsedKB)
        if len(max_pos)<len(pos):
            max_pos=pos
    
    return max_pos 

def eqQueryCheck(query,var_query):
    if query[0]==var_query[0] and len(query)==len(var_query) and len(query[1])==len(var_query[1]):
        for i in xrange(len(query[1])):
            if isVar(var_query[1][i]):continue
            else:
                if query[1][i]!=var_query[1][i]:
                    return False
        return True
    else: return False
    
def standardizeKb(parsedKB):
    for i in xrange(len(parsedKB)):
        for j in xrange(len(parsedKB[i])):
            if type(parsedKB[i][j]) is list:
                for k in xrange(len(parsedKB[i][j])):
                    if parsedKB[i][j][k].islower():
                        parsedKB[i][j][k]+=str(i)
    return parsedKB

def check_arguments(a,b):
    eq=True
    for i in xrange(len(a)):
        if a[i].islower() and b[i].islower():
            eq=True
        elif a[i].islower():
            eq=False
            break
        elif b[i].islower():
            eq=False
            break
        elif a[i][0].isupper() and b[i][0].isupper():
            if a[i]==b[i]:eq=True
            else:
                eq=False
                break
    return eq

def remove_redundancy(a):
    n=len(a)
    mkd=[True]*n
    for i in xrange(0,len(a),2):
        if mkd[i]:
            for j in xrange(2,n,2):
                if mkd[j] and i!=j:
                    if a[i]==a[j] and len(a[i+1])==len(a[j+1]):
                        
                        if check_arguments(a[i+1], a[j+1]):
                            mkd[j],mkd[j+1]=False,False                         
        else:continue            
    return [item for i,item in enumerate(a) if mkd[i]]
    
################################################################## Resolution Algorithm (DFS Approach)

def unify_sentences(predx,predy):
    var=dict()
    kbPredicate = copy(predy)
    predx=split_predicate(predx)
    predy=split_predicate(predy)

    for px in predx:
        for py in predy:
            
            if isComplement(copy(px), copy(py)):
                
                n=len(px[1])
                temp=var
                unifiable=False
                for i in xrange(n):
                    if isVar(px[1][i]) and isVar(py[1][i]):
                        if py[1][i] in temp.keys():
                            pass
                        else:
                            temp[py[1][i]]= px[1][i]
                                                    
                        unifiable=True
                    
                    elif isVar(px[1][i]):
                        if px[1][i] in temp.keys():
                            if temp[px[1][i]]!=py[1][i]:
                                unifiable=False
                                
                                return kbPredicate
                                break;
                        temp[px[1][i]]=py[1][i]
                        unifiable=True
                    
                    elif isVar(py[1][i]):
                        if py[1][i] in temp.keys():
                            if temp[py[1][i]]!=px[1][i]:
                                unifiable=False
                                return kbPredicate
                                break;
                        temp[py[1][i]]=px[1][i]
                        unifiable=True
                    else:
                        if px[1][i]!=py[1][i]:
                            unifiable=False
                            return kbPredicate
                            break;
                        else:
                            unifiable=True   
                if unifiable:
                    var=temp
                    predx.remove(px)
                    predy.remove(py)
                    
    result=predx+predy
    if len(result)>0:
        unify_var(result,var)
        result=combine_predicate(result)
        result=remove_redundancy(result)
#         print result
        return result
    else: return None
#     return None
    
def unify_var(query,var):
    for i in xrange(len(query)):
        for j in xrange(len(query[i][1])):
            if query[i][1][j] in var.keys():
                query[i][1][j]=var[query[i][1][j]]
    return 

def checkSingleUnification(queryArguments,queryPredicate,kbArguments,parsedKB):
    
    for i,predicate in enumerate(parsedKB):
        pos=0

        if queryPredicate[0] == predicate[pos] and len(predicate) == 2 and len(queryArguments[0])==len(kbArguments[i][0]):
            if len(filter(lambda var: var[0].islower(),kbArguments[i][0]))== len(queryArguments[0]):
                return True
            else:
                temp=parsedKB[i]
                for j,var in enumerate(kbArguments[i][0]):
                    if var[0].islower():
                        temp[1][j]=queryArguments[j][0]
                    elif var != queryArguments[j][0]:
                        return False
                
                return len(filter(lambda predicate: predicate == temp ,parsedKB))>0        
    
    return False

def resolveQuery(query,queryArguments,queryPredicate,kbArguments,parsedKB,ns):
    
    if checkSingleUnification(queryArguments,queryPredicate,kbArguments,parsedKB):
        return True
    
    else:
        contraQuery=copy(query)
        contraQuery[0]=complementQuery(contraQuery)
        pos=findComplement(queryPredicate[0], parsedKB)
        result=[] 
        visited=[True]*ns     
        def resolve_dfs(pos,changeKB,tempClause,visited,result):
            
#             if (time.time()-start>100):
#                 return False                         
            if len(pos)<1 and result!=None:
                return False
            
            if result==None:
                return True    
                   
            for p in pos:
                if visited[p]:
                            
                    result=unify_sentences(copy(tempClause),copy(changeKB[p]))
            
#                     print tempClause
#                     print changeKB[p],pos
#                     print p,result
#                     print
                    
                    if result==None:
                        return True
               
                    if eqQueryCheck(query,result):
                        return True
            
                    tempKB=copy(changeKB)
                    prevClause=copy(tempClause)
                    changeKB[p]=result
                    tempClause=result
                    visited[p]=False
                    
                    if resolve_dfs(findComplement_Sentence(result,changeKB),changeKB,tempClause,visited,result):
                        return True            
                    
                    tempClause=copy(prevClause)
                    changeKB=copy(tempKB)
                    visited[p]=True
                
                else:
                    continue    
            return False
   
    return resolve_dfs(pos,copy(parsedKB),copy(contraQuery),visited,result)
    
########################################################## File Operations    

def get_file_input():
    
    fin = open("input.txt","r")
    nq = int(fin.readline())
    queries=[]

    for _ in xrange(nq):
        queries.append((fin.readline()).strip())
    
    ns = int(fin.readline())
    sentences=[]
    
    for _ in xrange(0,ns):
        sentences.append((fin.readline()).strip())
    fin.close()
    
    return nq,queries,ns,sentences

def print_output(answers):
    
    fout = open("output.txt","w+")
    for answer in answers:
        if answer:
            fout.write("TRUE\n")
            print "TRUE"
        else:
            fout.write("FALSE\n")
            print "FALSE"
    fout.close()
    
    return 

#################################################################### Main

def main():
    
    nq,queries,ns,sentences = get_file_input()
    answers=[False]*nq
    parsedQueries=map(stringParseToTokens,queries)
    parsedKB=map(stringParseToTokens,sentences)
    parsedKB=standardizeKb(copy(parsedKB))
        
    kbArguments,queryArguments = map(findarguments,parsedKB),map(findarguments,parsedQueries)

    kbPredicates=map(findPredicate,parsedKB)
    queryPredicates=map(findPredicate,parsedQueries)
         
    for i,query in enumerate(parsedQueries):        
#         if i>1:break
        if isValid(queryPredicates[i],kbPredicates):
            if query in parsedKB:
                answers[i]=True
            else:
                answers[i]=resolveQuery(query,queryArguments[i],queryPredicates[i],kbArguments,parsedKB,ns)
        else:
            answers[i]=False
          
    print_output(answers)
    return
    
if __name__=='__main__':   
#     start=time.time()
    main() 
#     print "\nRun time: "+ str(time.time()-start)+" seconds"