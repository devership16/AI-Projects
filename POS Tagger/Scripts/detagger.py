################################################### File Operations

def get_corpus_data():
    
    fin = open("en_train_tagged.txt","r",encoding='utf8')
    corpus=[]
    for line in fin: 
        line=line.strip()
        sentence=[]
        tokens=line.split(' ')
        for token in tokens:
            word_tag=tuple(token.rsplit('/',1))
            sentence.append(word_tag[0])
        corpus.append(" ".join(sentence))
    
    fin.close()
    return corpus

def print_corpus(corpus):
    
    fout = open("en_train_raw.txt","w+",encoding='utf8')
    for line in corpus:
        fout.write((line)+"\n")
    fout.close()    
    return 

##################################################### Driver Function

def hmmlearn():    
    
    corpus=get_corpus_data()   
    print_corpus(corpus)
    return
