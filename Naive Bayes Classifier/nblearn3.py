import sys
import re
# import time
from collections import defaultdict
from string import punctuation

################################################### File Operations

def get_hotelReviews_data():
    
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
        reviews[hotelKey]=formatSentence(reviewText.strip())
#         reviews[hotelKey]=reviewText.strip()
        
        validity[hotelKey]=reviewValidity
        sentiment[hotelKey]=reviewSentiment
    
    fin.close()
    return reviews,validity,sentiment 

def print_nb_model(sentimentPriorProb,validityPriorProb,sentimentFeatureProb,validityFeatureProb):
    
    fout = open("nbmodel.txt","w+")
    
    fout.write("<#SENTIMENT-PRIOR#>\n")
    for sentiment in sentimentPriorProb.keys():
        fout.write(sentiment + " " + str(sentimentPriorProb[sentiment]) +"\n")
        
    fout.write("<#VALIDITY-PRIOR#>\n")
    for validity in validityPriorProb.keys():
        fout.write(validity + " " + str(validityPriorProb[validity]) +"\n")
    
    fout.write("<#SENITMENT-POSTERIOR#>\n")
    for sentiment in sentimentFeatureProb.keys():
        for word in sentimentFeatureProb[sentiment].keys():
            fout.write(sentiment + " " + word +" " +str(sentimentFeatureProb[sentiment][word]) +"\n")
    
    fout.write("<#VALIDITY-POSTERIOR#>\n")
    for validity in validityFeatureProb.keys():
        for word in validityFeatureProb[validity].keys():
            fout.write(validity + " " + word + " "+str(validityFeatureProb[validity][word]) +"\n")
    
    fout.close()
    return 

##################################################### Util Functions

def formatToken(token):
#     return token.lower()
    return (token.strip(punctuation)).lower()

def formatSentence(sentence):
    return " ".join([term  for token in sentence.split() for term in (re.sub('[^A-Za-z0-9\']+',' ',token).split())])
    

def get_feature_counts(reviews,validity,sentiment):
    
    stopwords={'a':1,'an':1,'and':1,'are':1,"as":1,"at":1,"be":1,"by":1,"for":1,"from":1,"has":1,"he":1,'i':1,"in":1,'is':1,'it':1,"it's":1,"of":1,"on":1,'that':1,'this':1,'the':1,'to':1,'was':1,'were':1,'will':1,'with':1}
    
    sentimentFeatureCount = defaultdict(lambda:defaultdict(int))
    validityFeatureCount = defaultdict(lambda:defaultdict(int))
    sentimentWordCount = defaultdict(int) 
    validityWordCount = defaultdict(int)
    sentimentPrior = defaultdict(int)
    validityPrior = defaultdict(int)
    
    for hotelKey in reviews.keys():
        
        review=reviews[hotelKey]        
        tokens=[token.strip() for token in review.split()]
        
        sentimentVal=sentiment[hotelKey]
        sentimentPrior[sentimentVal]+=1
        
        validityVal=validity[hotelKey]
        validityPrior[validityVal]+=1
        
        for token in tokens:
            
            word=formatToken(token)
            
            if word in stopwords.keys():
                continue
            
            if word:
                
                sentimentFeatureCount[sentimentVal][word]+=1
                validityFeatureCount[validityVal][word]+=1
                sentimentWordCount[sentimentVal]+=1
                validityWordCount[validityVal]+=1
        
        
    return sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount,sentimentPrior,validityPrior

def get_prior_probabilities(sentimentPrior,validityPrior):
    
    totalReviews=0.0
    sentimentPriorProb = defaultdict()
    validityPriorProb = defaultdict()
    
    for key in sentimentPrior.keys():
        totalReviews+=sentimentPrior[key]
    
    for key in sentimentPrior.keys():
        sentimentPriorProb[key]=float(sentimentPrior[key])/float(totalReviews)

    for key in validityPrior.keys():
        validityPriorProb[key]=float(validityPrior[key])/float(totalReviews)
        
    return sentimentPriorProb,validityPriorProb

def smoothingProbabilities(sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount):
    
    count=0
    for sentiment in list(sentimentFeatureCount.keys()):  
        
        if sentiment == "Pos":
            oppSentiment = "Neg"
        elif sentiment == "Neg":
            oppSentiment = "Pos"
        
        for word in (sentimentFeatureCount[sentiment].keys()):
            
            sentimentFeatureCount[sentiment][word]+=1
#             sentimentWordCount[sentiment]+=1
            
            if word not in sentimentFeatureCount[oppSentiment].keys():
                
                sentimentFeatureCount[oppSentiment][word] = count
                sentimentWordCount[oppSentiment]+=count
        
        sentimentWordCount[sentiment]+=len(sentimentFeatureCount[sentiment].keys())
        count+=1    

    count=0 
    for validity in list(validityFeatureCount.keys()):  
        if validity == "True":
            oppValidity = "Fake"
        elif validity == "Fake":
            oppValidity = "True"
        
        for word in (validityFeatureCount[validity].keys()):
            
            validityFeatureCount[validity][word]+=1
#             validityWordCount[validity]+=1
            
            if word not in validityFeatureCount[oppValidity].keys():
                
                validityFeatureCount[oppValidity][word] = count
                validityWordCount[oppValidity]+=count
               
        validityWordCount[validity]+=len(validityFeatureCount[validity].keys())
        count+=1
    
    return sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount

def get_posterior_probabilities(sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount):    
        
    sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount = smoothingProbabilities(sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount)
    
    sentimentFeatureProb = defaultdict(lambda:defaultdict(int))
    validityFeatureProb = defaultdict(lambda:defaultdict(int))
    
    for sentiment in sentimentFeatureCount.keys():
        for token in sentimentFeatureCount[sentiment].keys():
            sentimentFeatureProb[sentiment][token] = float(sentimentFeatureCount[sentiment][token])/float(sentimentWordCount[sentiment]) 
    
    for validity in validityFeatureCount.keys():
        for token in validityFeatureCount[validity].keys():
            validityFeatureProb[validity][token] = float(validityFeatureCount[validity][token])/float(validityWordCount[validity])        
    
    return sentimentFeatureProb, validityFeatureProb

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

##################################################### Driver Function

def nblearn():
    
    reviews,validity,sentiment = get_hotelReviews_data()
    
#     stopwords=getstopwords(reviews)
    
    sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount,sentimentPrior,validityPrior = get_feature_counts(reviews,validity,sentiment)
    
    sentimentPriorProb, validityPriorProb = get_prior_probabilities(sentimentPrior,validityPrior)
    sentimentFeatureProb, validityFeatureProb = get_posterior_probabilities(sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount)

    print_nb_model(sentimentPriorProb,validityPriorProb,sentimentFeatureProb,validityFeatureProb)
     
    return

if __name__=='__main__':   
    
#     start=time.time()
    nblearn() 
#     print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
