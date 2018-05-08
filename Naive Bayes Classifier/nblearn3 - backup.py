import sys
import re
import time
from collections import defaultdict
from string import punctuation

################################################### File Operations

def get_hotelReviews_data():
    
#     fin = open(sys.argv[1],"r")
    fin = open("train-labeled.txt","r")
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
    

def get_feature_counts(reviews,validity,sentiment,stopwords):
    
#     stopwords={'a': 1, 'able': 1, 'about': 1, 'above': 1, 'across': 1, 'again': 1, "ain't": 1, 'all': 1, 'almost': 1, 'along': 1, 'also': 1, 'am': 1, 'among': 1, 'amongst': 1, 'an': 1, 'and': 1, 'anyhow': 1, 'anyone': 1, 'anyway': 1, 'anyways': 1, 'appear': 1, 'are': 1, 'around': 1, 'as': 1, "a's": 1, 'aside': 1, 'ask': 1, 'asking': 1, 'at': 1, 'away': 1, 'be': 1, 'became': 1, 'because': 1, 'become': 1, 'becomes': 1, 'becoming': 1, 'been': 1, 'before': 1, 'behind': 1, 'below': 1, 'beside': 1, 'besides': 1, 'between': 1, 'beyond': 1, 'both': 1, 'brief': 1, 'but': 1, 'by': 1, 'came': 1, 'can': 1, 'come': 1, 'comes': 1, 'consider': 1, 'considering': 1, 'corresponding': 1, 'could': 1, 'do': 1, 'does': 1, 'doing': 1, 'done': 1, 'down': 1, 'downwards': 1, 'during': 1, 'each': 1, 'edu': 1, 'eg': 1, 'eight': 1, 'either': 1, 'else': 1, 'elsewhere': 1, 'etc': 1, 'even': 1, 'ever': 1, 'every': 1, 'ex': 1, 'few': 1, 'followed': 1, 'following': 1, 'follows': 1, 'for': 1, 'former': 1, 'formerly': 1, 'from': 1, 'further': 1, 'furthermore': 1, 'get': 1, 'gets': 1, 'getting': 1, 'given': 1, 'gives': 1, 'go': 1, 'goes': 1, 'going': 1, 'gone': 1, 'got': 1, 'gotten': 1, 'happens': 1, 'has': 1, 'have': 1, 'having': 1, 'he': 1, 'hed': 1, 'hence': 1, 'her': 1, 'here': 1, 'hereafter': 1, 'hereby': 1, 'herein': 1, "here's": 1, 'hereupon': 1, 'hers': 1, 'herself': 1, "he's": 1, 'hi': 1, 'him': 1, 'himself': 1, 'his': 1, 'how': 1, 'hows': 1, 'i': 1, "i'd": 1, 'ie': 1, 'if': 1, "i'll": 1, "i'm": 1, 'in': 1, 'inc': 1, 'indeed': 1, 'into': 1, 'inward': 1, 'is': 1, 'it': 1, "it'd": 1, "it'll": 1, 'its': 1, "it's": 1, 'itself': 1, "i've": 1, 'keep': 1, 'keeps': 1, 'kept': 1, 'know': 1, 'known': 1, 'knows': 1, 'lately': 1, 'later': 1, 'latter': 1, 'latterly': 1, 'lest': 1, 'let': 1, "let's": 1, 'looking': 1, 'looks': 1, 'ltd': 1, 'may': 1, 'maybe': 1, 'me': 1, 'mean': 1, 'meanwhile': 1, 'might': 1, 'most': 1, 'my': 1, 'myself': 1, 'name': 1, 'namely': 1, 'nd': 1, 'near': 1, 'nearly': 1, 'need': 1, 'needs': 1, 'neither': 1, 'next': 1, 'nine': 1, 'no': 1, 'non': 1, 'now': 1, 'nowhere': 1, 'of': 1, 'off': 1, 'often': 1, 'oh': 1, 'ok': 1, 'okay': 1, 'old': 1, 'on': 1, 'once': 1, 'one': 1, 'ones': 1, 'only': 1, 'onto': 1, 'or': 1, 'other': 1, 'others': 1, 'ought': 1, 'our': 1, 'ours': 1, 'ourselves': 1, 'out': 1, 'over': 1, 'own': 1, 'per': 1, 'placed': 1, 'que': 1, 'quite': 1, 're': 1, 'regarding': 1, 'said': 1, 'same': 1, 'saw': 1, 'say': 1, 'saying': 1, 'says': 1, 'second': 1, 'secondly': 1, 'see': 1, 'seeing': 1, 'seem': 1, 'seemed': 1, 'seeming': 1, 'seems': 1, 'seen': 1, 'self': 1, 'selves': 1, 'sensible': 1, 'sent': 1, 'seven': 1, 'several': 1, 'she': 1, "she'd": 1, "she'll": 1, "she's": 1, 'since': 1, 'six': 1, 'so': 1, 'some': 1, 'somebody': 1, 'somehow': 1, 'someone': 1, 'something': 1, 'sometime': 1, 'sometimes': 1, 'somewhat': 1, 'somewhere': 1, 'soon': 1, 'specified': 1, 'specify': 1, 'specifying': 1, 'still': 1, 'sub': 1, 'such': 1, 'sup': 1, 'sure': 1, 'take': 1, 'taken': 1, 'tell': 1, 'tends': 1, 'th': 1, 'than': 1, 'that': 1, 'thats': 1, "that's": 1, 'the': 1, 'their': 1, 'theirs': 1, 'them': 1, 'themselves': 1, 'then': 1, 'thence': 1, 'there': 1, 'thereafter': 1, 'thereby': 1, 'therefore': 1, 'therein': 1, 'theres': 1, "there's": 1, 'thereupon': 1, 'these': 1, 'they': 1, "they'd": 1, "they'll": 1, "they're": 1, "they've": 1, 'think': 1, 'third': 1, 'this': 1, 'those': 1, 'though': 1, 'three': 1, 'through': 1, 'thru': 1, 'thus': 1, 'to': 1, 'together': 1, 'too': 1, 'took': 1, 'toward': 1, 'towards': 1, 'tried': 1, 'tries': 1, 'truly': 1, 'try': 1, 'trying': 1, "t's": 1, 'twice': 1, 'two': 1, 'un': 1, 'under': 1, 'up': 1, 'upon': 1, 'us': 1, 'use': 1, 'used': 1, 'uses': 1, 'using': 1, 'usually': 1, 'value': 1, 'various': 1, 'very': 1, 'via': 1, 'viz': 1, 'vs': 1, 'want': 1, 'wants': 1, 'was': 1, "wasn't": 1, 'way': 1, 'we': 1, "we'd": 1, "we'll": 1, 'went': 1, 'were': 1, "we're": 1, "weren't": 1, "we've": 1, 'what': 1, 'whatever': 1, "what's": 1, 'when': 1, 'whence': 1, 'whenever': 1, "when's": 1, 'where': 1, 'whereafter': 1, 'whereas': 1, 'whereby': 1, 'wherein': 1, "where's": 1, 'whereupon': 1, 'wherever': 1, 'whether': 1, 'which': 1, 'while': 1, 'whither': 1, 'who': 1, 'whoever': 1, 'whole': 1, 'whom': 1, "who's": 1, 'whose': 1, 'why': 1, "why's": 1, 'will': 1, 'willing': 1, 'wish': 1, 'with': 1, 'within': 1, 'without': 1, "won't": 1, 'would': 1, "wouldn't": 1, 'yes': 1, 'yet': 1, 'you': 1, "you'd": 1, "you'll": 1, 'your': 1, "you're": 1, 'yours': 1, 'yourself': 1, 'yourselves': 1, "you've": 1}
#     stopwords={'a':1,'an':1,'and':1,'are':1,"as":1,"at":1,"be":1,"by":1,"for":1,"from":1,"has":1,"he":1,'i':1,"in":1,'is':1,'it':1,"it's":1,"of":1,"on":1,'that':1,'this':1,'the':1,'to':1,'was':1,'were':1,'will':1,'with':1}
#     stopwords={'the':1, 'and':1, 'to':1, 'a':1, 'i':1, 'was':1, 'in':1, 'hotel':1, 'of':1, 'we':1, 'for':1, 'room':1, 'it':1, 'at':1, 'my':1, 'is':1, 'that':1, 'this':1, 'had':1, 'with':1}
    
    sentimentFeatureCount = defaultdict(lambda:defaultdict(int))
    validityFeatureCount = defaultdict(lambda:defaultdict(int))
    sentimentWordCount = defaultdict(int) 
    validityWordCount = defaultdict(int)
    sentimentPrior = defaultdict(int)
    validityPrior = defaultdict(int)
    
    for hotelKey in reviews.keys():
        review=reviews[hotelKey]
        
#         tokens=[term.strip() for token in review.split() for term in re.sub('\.',' ',token).split()]
        tokens=[token.strip() for token in review.split()]
        
        sentimentVal=sentiment[hotelKey]
        sentimentPrior[sentimentVal]+=1
        
        validityVal=validity[hotelKey]
        validityPrior[validityVal]+=1
        
        for token in tokens:
            
            word=formatToken(token)
            
            if word in stopwords:
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
    
    stopwords=getstopwords(reviews)
    
    sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount,sentimentPrior,validityPrior = get_feature_counts(reviews,validity,sentiment,stopwords)
    
    sentimentPriorProb, validityPriorProb = get_prior_probabilities(sentimentPrior,validityPrior)
    sentimentFeatureProb, validityFeatureProb = get_posterior_probabilities(sentimentFeatureCount,validityFeatureCount,sentimentWordCount,validityWordCount)

    print_nb_model(sentimentPriorProb,validityPriorProb,sentimentFeatureProb,validityFeatureProb)
     
    return

if __name__=='__main__':   
    
    start=time.time()
    nblearn() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
