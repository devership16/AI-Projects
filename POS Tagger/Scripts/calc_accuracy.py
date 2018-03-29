import time
def get_corpus_data():
    
    fin1 = open("hmmoutput.txt","r",encoding='utf-8')
    tagged_corpus=[]
    
    for line in fin1: 
        line=line.strip()
        tokens=line.split(' ')
        for token in tokens:            
            word_tag=token.rsplit('/',1)
            tagged_corpus.append(word_tag)
    
    fin1.close()
    
    fin2 = open("hi_test_tagged.txt","r",encoding='utf-8')
    original_corpus=[]
    
    for line in fin2: 
        line=line.strip()
        tokens=line.split(' ')
        for token in tokens:            
            word_tag=token.rsplit('/',1)
            original_corpus.append(word_tag)
    
    fin2.close()
    
    return tagged_corpus,original_corpus

##################################################### Driver Function

def hmmlearn():
    tagged_corpus,original_corpus=get_corpus_data()
    total=len(original_corpus)
    count=0.0
#     print(tagged_corpus)
    if len(tagged_corpus)!=len(original_corpus):
        print("Tagged corpus has different length...\n")
    else:
        for i in range(len(original_corpus)):

            if original_corpus[i][0]!=tagged_corpus[i][0]:
                print("Wrong word order in the tagged corpus!!\n")
            else:
                if original_corpus[i][1]==tagged_corpus[i][1]:
                    count+=1
#                 else:
#                     print("\n\t\t\tINCORRECT TAG")
#                     print("Original word/tag pair: "+str(original_corpus[i])+"\n")
#                     print("Tagged by us word/tag pair: "+str(tagged_corpus[i])+"\n")
     
    accuracy = float(count/total) *  100.00
    
    print("\n Count= "+str(count)+"\t Incorrect= "+str(total-count))
    print("The accuracy is: "+str(accuracy)+" %") 
    
    return

if __name__=='__main__':   
    
    start=time.time()
    hmmlearn() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
