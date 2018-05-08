import sys
import re
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
#         untagged_corpus[review[0]]= " ".join(review[1:])
        untagged_corpus[review[0]]=formatSentence(" ".join(review[1:]))
    
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
    
def formatSentence(sentence):
    return " ".join([term  for token in sentence.split() for term in (re.sub('[^A-Za-z0-9\']+',' ',token).split())])

def nbclassifyUtil(untagged_corpus,sentimentPrior,validityPrior,sentimentPostProb,validityPostProb):
    
#     stopwords={'a': 1, 'able': 1, 'about': 1, 'above': 1, 'across': 1, 'again': 1, "ain't": 1, 'all': 1, 'almost': 1, 'along': 1, 'also': 1, 'am': 1, 'among': 1, 'amongst': 1, 'an': 1, 'and': 1, 'anyhow': 1, 'anyone': 1, 'anyway': 1, 'anyways': 1, 'appear': 1, 'are': 1, 'around': 1, 'as': 1, "a's": 1, 'aside': 1, 'ask': 1, 'asking': 1, 'at': 1, 'away': 1, 'be': 1, 'became': 1, 'because': 1, 'become': 1, 'becomes': 1, 'becoming': 1, 'been': 1, 'before': 1, 'behind': 1, 'below': 1, 'beside': 1, 'besides': 1, 'between': 1, 'beyond': 1, 'both': 1, 'brief': 1, 'but': 1, 'by': 1, 'came': 1, 'can': 1, 'come': 1, 'comes': 1, 'consider': 1, 'considering': 1, 'corresponding': 1, 'could': 1, 'do': 1, 'does': 1, 'doing': 1, 'done': 1, 'down': 1, 'downwards': 1, 'during': 1, 'each': 1, 'edu': 1, 'eg': 1, 'eight': 1, 'either': 1, 'else': 1, 'elsewhere': 1, 'etc': 1, 'even': 1, 'ever': 1, 'every': 1, 'ex': 1, 'few': 1, 'followed': 1, 'following': 1, 'follows': 1, 'for': 1, 'former': 1, 'formerly': 1, 'from': 1, 'further': 1, 'furthermore': 1, 'get': 1, 'gets': 1, 'getting': 1, 'given': 1, 'gives': 1, 'go': 1, 'goes': 1, 'going': 1, 'gone': 1, 'got': 1, 'gotten': 1, 'happens': 1, 'has': 1, 'have': 1, 'having': 1, 'he': 1, 'hed': 1, 'hence': 1, 'her': 1, 'here': 1, 'hereafter': 1, 'hereby': 1, 'herein': 1, "here's": 1, 'hereupon': 1, 'hers': 1, 'herself': 1, "he's": 1, 'hi': 1, 'him': 1, 'himself': 1, 'his': 1, 'how': 1, 'hows': 1, 'i': 1, "i'd": 1, 'ie': 1, 'if': 1, "i'll": 1, "i'm": 1, 'in': 1, 'inc': 1, 'indeed': 1, 'into': 1, 'inward': 1, 'is': 1, 'it': 1, "it'd": 1, "it'll": 1, 'its': 1, "it's": 1, 'itself': 1, "i've": 1, 'keep': 1, 'keeps': 1, 'kept': 1, 'know': 1, 'known': 1, 'knows': 1, 'lately': 1, 'later': 1, 'latter': 1, 'latterly': 1, 'lest': 1, 'let': 1, "let's": 1, 'looking': 1, 'looks': 1, 'ltd': 1, 'may': 1, 'maybe': 1, 'me': 1, 'mean': 1, 'meanwhile': 1, 'might': 1, 'most': 1, 'my': 1, 'myself': 1, 'name': 1, 'namely': 1, 'nd': 1, 'near': 1, 'nearly': 1, 'need': 1, 'needs': 1, 'neither': 1, 'next': 1, 'nine': 1, 'no': 1, 'non': 1, 'now': 1, 'nowhere': 1, 'of': 1, 'off': 1, 'often': 1, 'oh': 1, 'ok': 1, 'okay': 1, 'old': 1, 'on': 1, 'once': 1, 'one': 1, 'ones': 1, 'only': 1, 'onto': 1, 'or': 1, 'other': 1, 'others': 1, 'ought': 1, 'our': 1, 'ours': 1, 'ourselves': 1, 'out': 1, 'over': 1, 'own': 1, 'per': 1, 'placed': 1, 'que': 1, 'quite': 1, 're': 1, 'regarding': 1, 'said': 1, 'same': 1, 'saw': 1, 'say': 1, 'saying': 1, 'says': 1, 'second': 1, 'secondly': 1, 'see': 1, 'seeing': 1, 'seem': 1, 'seemed': 1, 'seeming': 1, 'seems': 1, 'seen': 1, 'self': 1, 'selves': 1, 'sensible': 1, 'sent': 1, 'seven': 1, 'several': 1, 'she': 1, "she'd": 1, "she'll": 1, "she's": 1, 'since': 1, 'six': 1, 'so': 1, 'some': 1, 'somebody': 1, 'somehow': 1, 'someone': 1, 'something': 1, 'sometime': 1, 'sometimes': 1, 'somewhat': 1, 'somewhere': 1, 'soon': 1, 'specified': 1, 'specify': 1, 'specifying': 1, 'still': 1, 'sub': 1, 'such': 1, 'sup': 1, 'sure': 1, 'take': 1, 'taken': 1, 'tell': 1, 'tends': 1, 'th': 1, 'than': 1, 'that': 1, 'thats': 1, "that's": 1, 'the': 1, 'their': 1, 'theirs': 1, 'them': 1, 'themselves': 1, 'then': 1, 'thence': 1, 'there': 1, 'thereafter': 1, 'thereby': 1, 'therefore': 1, 'therein': 1, 'theres': 1, "there's": 1, 'thereupon': 1, 'these': 1, 'they': 1, "they'd": 1, "they'll": 1, "they're": 1, "they've": 1, 'think': 1, 'third': 1, 'this': 1, 'those': 1, 'though': 1, 'three': 1, 'through': 1, 'thru': 1, 'thus': 1, 'to': 1, 'together': 1, 'too': 1, 'took': 1, 'toward': 1, 'towards': 1, 'tried': 1, 'tries': 1, 'truly': 1, 'try': 1, 'trying': 1, "t's": 1, 'twice': 1, 'two': 1, 'un': 1, 'under': 1, 'up': 1, 'upon': 1, 'us': 1, 'use': 1, 'used': 1, 'uses': 1, 'using': 1, 'usually': 1, 'value': 1, 'various': 1, 'very': 1, 'via': 1, 'viz': 1, 'vs': 1, 'want': 1, 'wants': 1, 'was': 1, "wasn't": 1, 'way': 1, 'we': 1, "we'd": 1, "we'll": 1, 'went': 1, 'were': 1, "we're": 1, "weren't": 1, "we've": 1, 'what': 1, 'whatever': 1, "what's": 1, 'when': 1, 'whence': 1, 'whenever': 1, "when's": 1, 'where': 1, 'whereafter': 1, 'whereas': 1, 'whereby': 1, 'wherein': 1, "where's": 1, 'whereupon': 1, 'wherever': 1, 'whether': 1, 'which': 1, 'while': 1, 'whither': 1, 'who': 1, 'whoever': 1, 'whole': 1, 'whom': 1, "who's": 1, 'whose': 1, 'why': 1, "why's": 1, 'will': 1, 'willing': 1, 'wish': 1, 'with': 1, 'within': 1, 'without': 1, "won't": 1, 'would': 1, "wouldn't": 1, 'yes': 1, 'yet': 1, 'you': 1, "you'd": 1, "you'll": 1, 'your': 1, "you're": 1, 'yours': 1, 'yourself': 1, 'yourselves': 1, "you've": 1}
    
    classificationResults=[]
    pos ='Pos'
    neg ='Neg'
    true = 'True'
    fake ='Fake'
    
    for key in untagged_corpus.keys():
        review = untagged_corpus[key]
        
#         tokens=[term.strip() for token in review.split() for term in re.sub('\.',' ',token).split()]
        tokens = [token.strip() for token in review.split()]
        
        posFeatureVal=sentimentPrior[pos]
        negFeatureVal=sentimentPrior[neg]
        trueFeatureVal=validityPrior[true]
        fakeFeatureVal=validityPrior[fake]
        sentiment=''
        validity=''
        
        for token in tokens:
            
            word=formatToken(token)
            
#             if word in stopwords.keys():
#                 continue

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
    