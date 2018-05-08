import sys
import re
# import time
from string import  punctuation 
from collections import defaultdict 

####################################################### File Operations

def get_percepModel_data():
    
#     fin = open("vanillamodel.txt","r")
#     fin = open("averagedmodel.txt","r")
    fin = open(sys.argv[1],"r")
    
    sBias = False
    sWeights= False
    vBias = False
    vWeights = False
    
    weightsSenti = defaultdict(int)
    weightsValidity = defaultdict(int)
    
    for line in fin:
        line=line.strip()
        
        if line =="<#SENTIMENT-BIAS#>":
            sBias = True
            sWeights= False
            vBias = False
            vWeights = False
            continue
        
        elif line == "<#VALIDITY-BIAS#>":
            sBias = False
            sWeights= False
            vBias = True
            vWeights = False
            continue
        
        elif line == "<#SENTIMENT-WEIGHTS#>":
            sBias = False
            sWeights= True
            vBias = False
            vWeights = False
            continue
        
        elif line == "<#VALIDITY-WEIGHTS#>":
            sBias = False
            sWeights= False
            vBias = False
            vWeights = True
            continue
        
        elif sBias:
            biasSenti = float(line.strip()) 
            continue
        
        elif sWeights:
            word, sProb=line.split()
            weightsSenti[word] = float(sProb)
            continue
        
        elif vBias:
            biasValidity = float(line.strip()) 
            continue
        
        elif vWeights:
            word, vProb = line.split()
            weightsValidity[word] = float(vProb)
            continue

    fin.close()
    
    return biasSenti, weightsSenti, biasValidity, weightsValidity

def get_input():
    
    fin = open(sys.argv[2],"r")
#     fin = open("dev-text.txt","r")
    
    untagged_corpus=defaultdict(int)
    
    for line in fin:
        review=(line.strip()).split()
        untagged_corpus[review[0]]=formatSentence(" ".join(review[1:])).split()
    
    fin.close()
    
    return untagged_corpus

def print_output(tagged_corpus):
    
    fout = open("percepoutput.txt","w+")
    
    for line in tagged_corpus:
        fout.write(str(line[0]) +" " + line[1] +" "+ line[2]+"\n")
    
    fout.close()    
    return

####################################################### Utils

def formatToken(token):
    return token.strip(punctuation).lower()
    
def formatSentence(sentence):
    return " ".join([formatToken(term.strip())  for token in sentence.split() for term in (re.sub('[^A-Za-z0-9\']+',' ',token).split())])

def runPerceptron(untagged_corpus, biasSenti, weightsSenti, biasValidity, weightsValidity):
    classificationResults=[]
    pos ="Pos"
    neg ="Neg"
    true = "True"
    fake ="Fake"
    
    for hotelKey in untagged_corpus.keys():
            
        x = defaultdict(int)
        sentiment=""
        validity=""
        
        tokens = untagged_corpus[hotelKey]
        for token in tokens:
            x[token]+=1
        
        aSenti = biasSenti
        aValidity = biasValidity
        
        for key in x.keys():  
            
            aSenti +=  (weightsSenti[key] * x[key]) 
            aValidity +=  (weightsValidity[key] * x[key])
        
        sentiment = pos if aSenti > 0 else neg
        validity = true if aValidity > 0 else fake
    
        classificationResults.append([hotelKey,validity,sentiment])
    return classificationResults
        
####################################################### Driver Functions

def percepclassify():
    
    biasSenti, weightsSenti, biasValidity, weightsValidity = get_percepModel_data()
    untagged_corpus = get_input()
    
    tagged_corpus =  runPerceptron(untagged_corpus, biasSenti, weightsSenti, biasValidity, weightsValidity)
    print_output(tagged_corpus)
    
    return

if __name__=='__main__':   
    
#     start=time.time()
    percepclassify() 
#     print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
    