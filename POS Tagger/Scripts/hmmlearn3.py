import sys
import time
from collections import defaultdict 
# import math

################################################### File Operations

def get_corpus_data():
    
#     fin = open(sys.argv[1],"r",encoding='utf8')
    fin = open("hi_train_dev_tagged.txt","r",encoding='utf-8')
    corpus=[]
    transitions = defaultdict(int)
    tag_counts = defaultdict(int)
    emissions = defaultdict(int)
    
    for line in fin: 
        line=line.strip()
        corpus.append(line)
        
        tokens=line.split(' ')
        prevTag="<start>"
        for token in tokens:
            
            word_tag=tuple(token.rsplit('/',1))
            tag = word_tag[1]
            tag_counts[tag]+=1
            emissions[word_tag]+=1
            transitions[(prevTag,tag)]+=1
            prevTag=tag
        
        transitions[(prevTag,"<end>")]+=1
    
    tag_counts["<start>"]=len(corpus)
    tag_counts["<end>"]=len(corpus)
    
    fin.close()
    return emissions,transitions,tag_counts

def print_hmm_model(tag_counts,emissionsProb,transitionsProb):
    
    fout = open("hmmmodel.txt","w+",encoding='utf-8')
    
    fout.write("<#TRANSITIONS#>\n")
    for transition in  transitionsProb.keys():
        fout.write(transition[0] + " " + transition[1] + " " + str(transitionsProb[transition]) + "\n")
    
    fout.write("<#EMISSIONS#>\n")
    for emission in  emissionsProb.keys():
        fout.write(emission[0] + " " + emission[1] + " " + str(emissionsProb[emission]) + "\n")    
    
    fout.write("<#TAGS#>\n")
    for tag in  tag_counts.keys():
        fout.write(tag + " " + str(tag_counts[tag]) + "\n")
 
    fout.close()    
    return 

##################################################### Util Functions

def calc_emissionProbabilities(emissions,tag_counts):
    
    emissionsProb = defaultdict(int)   
    for emission in emissions.keys():
        
        numerator = emissions[emission]
        denominator = tag_counts[emission[1]]

        emissionsProb[emission] = (numerator/denominator)

    return emissionsProb
    
def calc_transitionProbabilties(transitions,tag_counts):
    transitionsProb = defaultdict(int)
    transitions,tag_counts=smoothingTransitions(transitions, tag_counts)
    for transition in transitions:
        numerator = transitions[transition]   
        denominator = tag_counts[transition[0]]

        transitionsProb[transition] = (numerator/denominator)
    
    return transitionsProb

def smoothingTransitions(transitions,tag_counts):
    
    for tag1 in tag_counts.keys():
        for tag2 in tag_counts.keys():
            transitions[(tag1,tag2)]+=1
            tag_counts[tag1]+=1
    
    return transitions,tag_counts

##################################################### Driver Function

def hmmlearn():
    
    emissions,transitions,tag_counts=get_corpus_data()   
    
    emissionsProb = calc_emissionProbabilities(emissions, tag_counts)
    
    transitionsProb = calc_transitionProbabilties(transitions, tag_counts)
    
    tag_counts.__delitem__("<start>")
    tag_counts.__delitem__("<end>")
    
    print_hmm_model(tag_counts,emissionsProb,transitionsProb)    
    
    return

if __name__=='__main__':   
    
    start=time.time()
    hmmlearn() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
