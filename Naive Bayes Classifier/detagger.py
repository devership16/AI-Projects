import time
################################################### File Operations

def get_corpus_data():
    
    fin = open("train-labeled.txt","r")
    corpus=[]
    for line in fin: 
        line=line.strip()
#         print(line[:7]+line[16:])
        corpus.append(line[:16])
#         corpus.append(line[:7]+line[16:])
    fin.close()
    return corpus

def print_corpus(corpus):
    
#     fout = open("train-text.txt","w+")
    fout = open("train-key.txt","w+")
    for line in corpus:
        fout.write((line)+"\n")
    fout.close()    
    return 

##################################################### Driver Function

def detagger():    
    
    corpus=get_corpus_data()   
    print_corpus(corpus)
    return
if __name__=='__main__':   
    
    start=time.time()
    detagger() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  