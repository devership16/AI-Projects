import time
def get_corpus_data():
    
    fin1 = open("nboutput.txt","r")
    tagged_corpus=[]
    
    for line in fin1: 
        line=line.strip()
        tagged_corpus.append(line.split(' '))
    
    fin1.close()
    
    fin2 = open("dev-key.txt","r")
    original_corpus=[]
    
    for line in fin2: 
        line=line.strip()
        original_corpus.append(line.split(' '))
    
    fin2.close()
    
    return tagged_corpus,original_corpus

##################################################### Driver Function

def nb_calc_accuracy():
    tagged_corpus,original_corpus=get_corpus_data()
    total=len(original_corpus)
    count=0.0
    validity=0.0
    sentiment=0.0
#     print(tagged_corpus)
    if len(tagged_corpus)!=len(original_corpus):
        print("Tagged corpus has different length...\n")
    else:
        for i in range(len(original_corpus)):

            if original_corpus[i][0]!=tagged_corpus[i][0]:
                print("Hotel Key mismatch...Wrong order in the tagged corpus!!\n")
            else:
                if original_corpus[i][1]==tagged_corpus[i][1] and original_corpus[i][2]==tagged_corpus[i][2]:
                    count+=1
                    validity+=1
                    sentiment+=1
                    continue
                elif original_corpus[i][1]==tagged_corpus[i][1]:
                    validity+=1
                    print("\t\tSentiment Feature Mismatch: "+original_corpus[i][0])
                    continue
                elif original_corpus[i][2]==tagged_corpus[i][2]:
                    sentiment+=1
                    print("\t\tValidity Feature Mismatch: "+original_corpus[i][0])
                    continue
                else:
                    print("\t\t\tTotal Mismatch... "+ original_corpus[i][0])
                    continue
     
    accuracy = float(count/total) *  100.00
    validityFeature = float(validity/total) * 100.00
    sentimentFeature = float(sentiment/total) * 100.00
    
    print("\nTotal="+str(total)+"\tCorrect = "+str(count)+"\t Incorrect= "+str(total-count))
    print("Validity % = "+str(validityFeature)+"\tCorrect = "+str(validity)+"\t Incorrect= "+str(total-validity))
    print("Senitment % = "+str(sentimentFeature)+"\tCorrect = "+str(sentiment)+"\t Incorrect= "+str(total-sentiment))
    
    print("The accuracy is: "+str(accuracy)+" %") 
    
    return

if __name__=='__main__':   
    
    start=time.time()
    nb_calc_accuracy() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
