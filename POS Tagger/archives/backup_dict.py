import sys
import time
import math
from collections import defaultdict 

####################################################### File Operations

def get_model_data():
    
    fin = open("hmmmodel.txt","r",encoding='utf8')

    transitionsProb = defaultdict(lambda:defaultdict(int))
    emissionsProb = defaultdict(lambda:defaultdict(int))
    tag_count = defaultdict(int)
    Tflag = False
    Eflag = False
    tagFlag = False
    
    for line in fin: 
        line=line.strip()
        if line=="<#TRANSITIONS#>":
            Tflag = True
            Eflag = False
            tagFlag = False
            continue
            
        elif line=="<#EMISSIONS#>":
            Tflag=False
            Eflag=True
            tagFlag = False
            continue
        
        elif line=="<#TAGS#>":
            Tflag=False
            Eflag=False
            tagFlag = True
            continue
        
        
        elif Tflag:
            t1,t2,tProb=line.split()
            transitionsProb[t1][t2]=float(tProb)
        
        elif Eflag:   
            word,tag,eProb=line.split()
            emissionsProb[word][tag]=float(eProb) 
            
        elif tagFlag:
            tag,count = line.split()
            tag_count[tag] = int(count)
                        
    fin.close()
    return emissionsProb,transitionsProb,tag_count

def get_input():
#     fin = open(sys.argv[-1],"r",encoding='utf8')
    fin = open("en_dev_raw.txt","r",encoding='utf8')
    untagged_data=[]
    for line in fin:
        
#         line=line.strip()
        untagged_data.append(line.strip())
    
    fin.close()
    
    return untagged_data

def print_output(tagged_corpus):
    
    fout = open("hmmoutput.txt","w+",encoding='utf8')
    for sentence in tagged_corpus:
        fout.write(sentence+"\n")
    fout.close()    
    return

####################################################### Utils

def findInitialProbs(token,emissionsProb,transitionsProb):
    
    states=[]
    initialEmission=defaultdict(int)
    for emission in emissionsProb.keys():
        if token == emission[0]:
            states.append(emission[1])
            initialEmission[emission]=emissionsProb[emission]
    
    start="<start>"
    initialTrans=defaultdict(int)
    for state in states:
        if (start,state) in transitionsProb.keys():
            initialTrans[(start,state)]=transitionsProb[(start,state)]
    
    initialProbs=defaultdict(int)
    for emission in initialEmission.keys():
        initialProbs[(0,emission)] = (initialEmission[emission]) * (initialTrans[(start,emission[1])]) 
    
    return initialProbs

def findEmissionStates(token, emissionsProb):
    return [emission for emission in emissionsProb[token].keys()]
    
def viterbi_decode(untagged_data,emissionsProb,transitionsProb,all_tags):
    tags=[]
    for sentence in untagged_data:
        
        sentence_tags=[]
        tokens = sentence.split()
        tokens=["<start>"]+tokens
#         prior = findInitialProbs(tokens[0],emissionsProb,transitionsProb)
        prior=defaultdict(int)
        prior[(0,("<start>","<start>"))] = 1.00
        
        backptr=defaultdict(str)
        prevstates=["<start>"]

        for index in range(1,len(tokens)):
            
            unknownFlag=False
            emissionStates=findEmissionStates(tokens[index],emissionsProb)
            
            if len(emissionStates) == 0: 
                emissionStates = all_tags
                unknownFlag=True

            for curr_state in emissionStates:
                max_val= -float('inf')
                back_state=""
                for prev_state in prevstates: 
                    
                    if unknownFlag:
                        (emissionsProb[tokens[index]][curr_state]) = 1
                    temp = (prior[(index-1,(tokens[index-1],prev_state))]) * (transitionsProb[prev_state][curr_state]) * (emissionsProb[tokens[index]][curr_state])
                     
                    if max_val<temp:
                        max_val=temp
                        back_state=prev_state
                backptr[(index,(tokens[index],curr_state))] = back_state
                prior[(index,(tokens[index],curr_state))] = max_val
            prevstates = emissionStates
         
        total_max=-float('inf')
        for end_state in prevstates:
            temp = prior[(index+1,(tokens[index],end_state))] * transitionsProb[end_state]["<end>"]
            if total_max < temp:
                total_max = temp
                final_state = end_state
                end_index=index
         
        state=final_state
                 
        while state != "<start>":
            sentence_tags.append(state)
            for ptr in backptr.keys():
                if ptr[1][1] == state and ptr[0] == end_index:
                    state = backptr[ptr]
                    break
            end_index -=1    
        tags.append(sentence_tags[::-1])
    return tags
            
def formatData(untagged_data,tags):
    tagged_data=[]
    for i in range(len(untagged_data)):
        sentence=[]
        tokens=untagged_data[i].split()
        for j in range(len(tokens)):
            sentence.append(str(tokens[j] + "/" +tags[i][j]))
        tagged_data.append(" ".join(sentence))
    
    return tagged_data

####################################################### Driver Functions

def hmmdecode():
    
    emissionsProb,transitionsProb,tag_count=get_model_data()
    untagged_data = get_input()
    all_tags = [key for key in tag_count.keys()]
    tags = viterbi_decode(untagged_data,emissionsProb,transitionsProb,all_tags)
    
    print_output(formatData(untagged_data,tags))
    
    return


if __name__=='__main__':   
    
    start=time.time()
    hmmdecode() 
    print ("\nRun time: "+ str(time.time()-start)+" seconds" )  
    