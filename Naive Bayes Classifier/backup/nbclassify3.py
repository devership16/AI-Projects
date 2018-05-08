import sys
import time
from math import log
from string import  punctuation 
from collections import defaultdict 

####################################################### File Operations

def get_nbmodel_data():
    
    fin = open("nbmodel.txt","r")
    sentimentPostProb = defaultdict(lambda:defaultdict(int))
    validityPostProb = defaultdict(lambda:defaultdict(int))
    sentimentPrior = defaultdict(int)
    validityPrior = defaultdict(int)
    
    sPrior=True
    vPrior=False
    sPost=False
    vPost=False
    
    for line in fin:
        line=line.strip()
        
        if line =="<#SENTIMENT-PRIOR#>":
            sPrior = True
            vPrior = False
            sPost = False
            vPost = False
            continue
        
        elif line == "<#VALIDITY-PRIOR#>":
            sPrior = False
            vPrior = True
            sPost = False
            vPost = False
            continue
        
        elif line == "<#SENITMENT-POSTERIOR#>":
            sPrior = False
            vPrior = False
            sPost = True
            vPost = False
            continue
        
        elif line == "<#VALIDITY-POSTERIOR#>":
            sPrior = False
            vPrior = False
            sPost = False
            vPost = True
            continue
        
        elif sPrior:
            sentiment,sProb=line.split()
            sentimentPrior[sentiment]=log(float(sProb))
            continue
        
        elif vPrior:
            validity,vProb=line.split()
            validityPrior[validity]=log(float(vProb))
            continue
        
        elif sPost:
            sentiment,word,sProb=line.split()
            sentimentPostProb[word][sentiment]=log(float(sProb))
            continue
        
        elif vPost:
            validity,word,vProb=line.split()
            validityPostProb[word][validity]=log(float(vProb))
            continue

    fin.close()
    return sentimentPrior,validityPrior,sentimentPostProb,validityPostProb

def get_input():
    
#     fin = open(sys.argv[1],"r")
    fin = open("dev-text.txt","r")
    untagged_corpus=defaultdict()
    
    for line in fin:
        review=(line.strip()).split()
        untagged_corpus[review[0]]= " ".join(review[1:])
    
    fin.close()
    
    return untagged_corpus

def print_output(tagged_corpus):
    
    fout = open("nboutput.txt","w+")
    
    for line in tagged_corpus:
        fout.write(str(line[0]) +" " + line[1] +" "+ line[2]+"\n")
    
    fout.close()    
    return

####################################################### Utils

def formatToken(token):
    return token.strip(punctuation).lower()
    
def nbclassifyUtil(untagged_corpus,sentimentPrior,validityPrior,sentimentPostProb,validityPostProb):
   
    classificationResults=[]
    pos ='Pos'
    neg ='Neg'
    true = 'True'
    fake ='Fake'
    
    for key in untagged_corpus.keys():
        
        tokens = [token.strip() for token in untagged_corpus[key].split()]
        
        posFeatureVal=sentimentPrior[pos]
        negFeatureVal=sentimentPrior[neg]
        trueFeatureVal=validityPrior[true]
        fakeFeatureVal=validityPrior[fake]
        sentiment=''
        validity=''
        
        for token in tokens:
            
            word=formatToken(token)

            if word:
                
                if sentimentPostProb[word][pos] is not None:
                    posFeatureVal+=sentimentPostProb[word][pos]        
                
                if sentimentPostProb[word][neg] is not None:
                    negFeatureVal+=sentimentPostProb[word][neg]
                
                if validityPostProb[word][true] is not None:
                    trueFeatureVal+=validityPostProb[word][true]
                
                if validityPostProb[word][fake] is not None:
                    fakeFeatureVal+=validityPostProb[word][fake]
        
        sentiment = pos if posFeatureVal>negFeatureVal else neg
        validity = true if trueFeatureVal>fakeFeatureVal else fake
        
        classificationResults.append([key,validity,sentiment])
                
    return classificationResults
   

####################################################### Driver Functions

def nbclassify():
    
    sentimentPrior,validityPrior,sentimentPostProb,validityPostProb = get_nbmodel_data()
    untagged_corpus = get_input()
    
    tagged_corpus =  nbclassifyUtil(untagged_corpus,sentimentPrior,validityPrior,sentimentPostProb,validityPostProb)
    print_output(tagged_corpus)
    
    return


if __name__=='__main__':   
    
    start=time.time()
    nbclassify() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
    