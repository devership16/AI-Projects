import sys
import re
import time
from collections import defaultdict
from string import punctuation

################################################### File Operations

def get_hotelReviews():
    
    fin = open(sys.argv[1],"r")
#     fin = open("train-labeled.txt","r")

    reviews=defaultdict(str)
    validity=defaultdict(str)
    sentiment=defaultdict(str)
    
    for line in fin:
        hotelKey=line[:7]
        reviewValidity=line[8:12]
        reviewSentiment=line[13:16]
        reviewText=line[17:]
        reviews[hotelKey]=removeStopwords(formatSentence(reviewText.strip())).split()
#         reviews[hotelKey]=reviewText.strip()
        
        validity[hotelKey]=reviewValidity
        sentiment[hotelKey]=reviewSentiment
    
    fin.close()
    return reviews,validity,sentiment 

def print_perceptron_model(model,weightsSenti,biasSenti,weightsValid,biasValidity):
    
    fout = open(model,"w+")
        
    fout.write("<#SENTIMENT-BIAS#>\n")
    fout.write(str(biasSenti) + "\n")
    
    fout.write("<#SENTIMENT-WEIGHTS#>\n")
    for key in weightsSenti.keys():
        fout.write(key + " " + str(weightsSenti[key]) + "\n")
        
    fout.write("<#VALIDITY-BIAS#>\n")
    fout.write(str(biasValidity) + "\n")
    
    fout.write("<#VALIDITY-WEIGHTS#>\n")
    for key in weightsValid.keys():
        fout.write(key + " " + str(weightsValid[key]) + "\n")
        
    fout.close()
    return 

##################################################### Util Functions

def formatToken(token):
    return (token.strip(punctuation)).lower()

def formatSentence(sentence):
    return " ".join([formatToken(term.strip()) for token in sentence.split() for term in (re.sub('[^A-Za-z0-9\']+',' ',token).split())])
     
def removeStopwords(sentence):
    stopwords={'a':1,'an':1,'and':1,'are':1,"as":1,"at":1,"be":1,"by":1,"for":1,"from":1,"has":1,"he":1,"in":1,'is':1,'it':1,"its":1,"of":1,"on":1,'that':1,'this':1,'the':1,'to':1,'was':1,'were':1,'will':1,'with':1}
    tempSent = sentence.split()
    res = []
    for word in tempSent:
        if word in stopwords.keys():
            continue
        res.append(word)
    return " ".join(res)
    
def getstopwords(reviews):
    stopwords=defaultdict(int)
     
    for key in reviews.keys():
        review= reviews[key]
        tokens=[token.strip() for token in review.split()]
        
        for token in tokens:
            word=formatToken(token)
            if word:
                stopwords[word]+=1
    
    return list(sorted(stopwords,key=stopwords.get,reverse=True))[:20]

def learnPerceptronParameters(reviews,validity,sentiment):
    
    stopwords={'a':1,'an':1,'and':1,'are':1,"as":1,"at":1,"be":1,"by":1,"for":1,"from":1,"has":1,"he":1,"in":1,'is':1,'it':1,"it's":1,"of":1,"on":1,'that':1,'this':1,'the':1,'to':1,'was':1,'were':1,'will':1,'with':1}
    
    biasVSenti = 0
    biasVValidity = 0
    
    weightsVSenti = defaultdict(int)
    weightsVValid = defaultdict(int)
    
    weightsASenti = defaultdict(int)
    weightsAValid = defaultdict(int)
    
    tempBiasSenti = 0
    tempBiasValidity = 0
    
    tempWeightsSenti = defaultdict(int)
    tempWeightsValid = defaultdict(int)
    
    iterNum = 30
    c = 1
    
    for _ in range(iterNum):
       
        for hotelKey in sorted(reviews.keys()):
            
            x = defaultdict(int)
            
            tokens = reviews[hotelKey]
            sentimentVal=sentiment[hotelKey]
            validityVal=validity[hotelKey]
            
            if sentimentVal == "Pos": ySenti = 1
            else: ySenti = -1
            
            if validityVal == "True": yValid = 1
            else: yValid = -1
            
            for token in tokens:
#                 if token in stopwords.keys():
#                     continue 
                x[token]+=1
            
            aSenti = biasVSenti
            aValid = biasVValidity
            
            for key in x.keys():
                
                aSenti = aSenti +  (weightsVSenti[key] * x[key]) 
                aValid = aValid + (weightsVValid[key] * x[key]) 
                
            if (yValid * aValid) <= 0:
               
                biasVValidity = biasVValidity + yValid
                tempBiasValidity = tempBiasValidity + (yValid * c)
                
                for token in x.keys():    
                    weightsVValid[token] = weightsVValid[token] + (yValid * x[token])
                    tempWeightsValid[token] = tempWeightsValid[token] + (yValid * c * x[token])
                    
                            
            if (ySenti * aSenti) <= 0:
                
                biasVSenti = biasVSenti + ySenti
                tempBiasSenti = tempBiasSenti + (ySenti * c)
                
                for token in x.keys():            
                    weightsVSenti[token] = weightsVSenti[token] + (ySenti * x[token])
                    tempWeightsSenti[token] = tempWeightsSenti[token] + (ySenti * c * x[token])
                        
            c+=1
    
    biasASenti = biasVSenti - (tempBiasSenti/float(c))
    for skey in tempWeightsSenti.keys():
        weightsASenti[skey] = float(weightsVSenti[skey]) - (tempWeightsSenti[skey]/float(c)) 
        
    biasAValidity = biasVValidity - float(tempBiasValidity/float(c))
    
    for vkey in tempWeightsValid.keys():
        weightsAValid[vkey] = float(weightsVValid[vkey])  - (tempWeightsValid[vkey]/float(c))  
     
    return weightsVSenti, biasVSenti, weightsVValid, biasVValidity, weightsASenti, biasASenti, weightsAValid, biasAValidity



##################################################### Driver Function

def perceplearn():
    
    reviews,validity,sentiment = get_hotelReviews()
#     stopwords=getstopwords(reviews)
    weightsVSenti, biasVSenti, weightsVValid, biasVValidity, weightsASenti, biasASenti, weightsAValid, biasAValidity = learnPerceptronParameters(reviews,validity,sentiment)
    
    model = "vanillamodel.txt"
    print_perceptron_model(model,weightsVSenti,biasVSenti,weightsVValid,biasVValidity)
    
    model = "averagedmodel.txt"
    print_perceptron_model(model,weightsASenti,biasASenti,weightsAValid,biasAValidity)
    
    return



if __name__=='__main__':   
    
    start=time.time()
    perceplearn() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
