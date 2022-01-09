###################################
# CS B551 Spring 2021, Assignment #3
#
# Vaibhav Vishwanath : 2000912419
#
# (Based on skeleton code by D. Crandall)
#


import random
import math
import re


# We've set up a suggested code structure, but feel free to change it. Just
# make sure your code still works with the label.py and pos_scorer.py code
# that we've supplied.
#I've referred the following links : 
#https://github.com/sumeetmishra199189/Elements-of-AI/tree/master/Probability
# Prof. David's viterbi_sol.py
#I have also taken help from a friend to understand Gibbs Sampling Code



class Solver:
    initial_pos={}
    priors={}
    transition_probabilities={}
    emission_probabilities={}
    transition_probabilities_gibbs={}
    word_speech={}
    s_list=['noun','adv','adp','x','.','conj','verb','det','num','pron','prt','adj']
    # Calculate the log of the posterior probability of a given sentence
    #  with a given part-of-speech labeling. Right now just returns -999 -- fix this!
    def __init__(self):
        pass
    
    # Posterior Calculation 
    def posterior(self, model, sentence, label):
        if model == "Simple":
            post_prob=0
            for word in sentence:
                for speech in label:
                    if word in self.emission_probabilities[speech]:
                        post_prob+=(math.log10(self.emission_probabilities[speech][word]) + math.log10(self.priors[speech]))
                    else:
                        post_prob+=(math.log10(1e-6)+math.log10(self.priors[speech]))
            return post_prob
        elif model == "HMM":
            post_prob=0
            for word in sentence:
                for speech in label:
                    if word in self.emission_probabilities[speech]:
                        post_prob+=(math.log10(self.emission_probabilities[speech][word]) + math.log10(self.priors[speech]))
                    else:
                        post_prob+=(math.log10(1e-6)+math.log10(self.priors[speech]))
            return post_prob
        elif model == "Complex":
            post_prob=0
            for word in sentence:
                for speech in label:
                    if word in self.emission_probabilities[speech]:
                        post_prob+=(math.log10(self.emission_probabilities[speech][word]) + math.log10(self.priors[speech]))
                    else:
                        post_prob+=(math.log10(1e-6)+math.log10(self.priors[speech]))
            return post_prob
        else:
            print("Unknown algo!")

    def get_initial_pos(self,data):
        i_pos={}
        i_pos_count={}
        for sentence,pos in data:
            for j in range(0,1):
                if pos[j] in i_pos_count:
                    i_pos_count[pos[j]]+=1
                else:
                    i_pos_count[pos[j]]=1
        for s in i_pos_count:
            i_pos[s]= i_pos_count[s]/sum(i_pos_count.values())
        #print(i_pos_count)
        #print(i_pos)
        return i_pos
    
    def get_priors(self,data):
        prior={}
        prior_count={}
        for sentence,pos in data:
            for j in range(len(sentence)):
                if pos[j] in prior_count:
                    prior_count[pos[j]]+=1
                else:
                    prior_count[pos[j]]=1
        for pos in prior_count:
            prior[pos]=prior_count[pos]/sum(prior_count.values())
        #print(prior_count)
        #print(prior)
        return prior
    
    def get_transition_prob(self,data):
        transition_counts={}
        transition_prob={}
        for speech in self.s_list:
            transition_counts[speech]={}
            for sentence,pos in data:
                for j in range(len(sentence)-1):
                    if speech==pos[j]:
                        if pos[j+1] in transition_counts[speech]:
                            transition_counts[speech][pos[j+1]]+=1
                        else:
                            transition_counts[speech][pos[j+1]]=1
        for pos in transition_counts:
            transition_prob[pos]={}
            for speech in transition_counts[pos]:
                transition_prob[pos][speech]=float(transition_counts[pos][speech])/sum(transition_counts[pos].values())
        #print(transition_counts)
        #print(transition_prob)
        return transition_prob
    
    def get_emission_prob(self,data):
        emission_counts={}
        emission_prob={}
        for speech in self.s_list:
            emission_counts[speech]={}
            for sentence,pos in data:
                for word,s in zip(sentence,pos):
                    if speech==s:
                        if word in emission_counts[speech]:
                            emission_counts[speech][word]+=1
                        else:
                            emission_counts[speech][word]=1
        for pos in emission_counts:
            emission_prob[pos]={}
            for word in emission_counts[pos]:
                emission_prob[pos][word]=float(emission_counts[pos][word])/sum(emission_counts[pos].values())
        #print(emission_counts)
        #print(emission_prob)
        return emission_prob

    def get_transition_gibbs(self,data):
        transition_counts_gibbs={}
        transition_prob_gibbs={}
        for speech in self.s_list:
            transition_counts_gibbs[speech]={}
            for sentence,pos in data:
                for j in range(len(sentence)-2):
                    if speech==pos[j]:
                        if pos[j+2] in transition_counts_gibbs[speech]:
                            transition_counts_gibbs[speech][pos[j+2]]+=1
                        else:
                            transition_counts_gibbs[speech][pos[j+2]]=1
        for pos in transition_counts_gibbs:
            transition_prob_gibbs[pos]={}
            for speech in transition_counts_gibbs[pos]:
                transition_prob_gibbs[pos][speech]=float(transition_counts_gibbs[pos][speech])/sum(transition_counts_gibbs[pos].values())
        #print(transition_counts_gibbs)
        #print(transition_prob_gibbs)
        return transition_prob_gibbs

    def get_word_speech(self,data):
        word_speech_count={}
        word_speech_prob={}
        for w,s in data:
            for j in range(len(w)):
                word_speech_count[w[j]]={}
                if s[j] in word_speech_count[w[j]]:
                    word_speech_count[w[j]][s[j]]+=1
                else:
                    word_speech_count[w[j]][s[j]]=1
        for w in word_speech_count:
            #print(w)
            for k in word_speech_count[w]:
                word_speech_prob[w]={}
                #print(k)
                word_speech_prob[w][k]=word_speech_count[w][k]/sum(word_speech_count[w].values())  
        #print(word_speech_count)
        #print(word_speech_prob)
        return word_speech_prob
    
    
    
    # Do the training! 
    # I have used functions to generate counts and probailities of priors, initial_pos used in Gibbs Sampling, transition_probabilities, and emission probabilities
    def train(self,data):
        self.initial_pos=self.get_initial_pos(data)
        self.priors=self.get_priors(data)
        self.transition_probabilities=self.get_transition_prob(data)
        self.emission_probabilities=self.get_emission_prob(data)
        self.transition_probabilities_gibbs=self.get_transition_gibbs(data)
        self.word_speech=self.get_word_speech(data)

            

    # Functions for each algorithm. Right now this just returns nouns -- fix this!
    def simplified(self, sentence):
        #print(sentence)
        #print(self.word_given_speech)
        l=[""]*len(sentence)
        
        idx=0
        for w in sentence:
            prob_speech_given_word=[]
            for speech in self.s_list:
            
                if w not in self.emission_probabilities[speech]:
                    self.emission_probabilities[speech][w]=1e-6
                prob_speech_given_word.append((speech,self.emission_probabilities[speech][w]*self.priors[speech]))
            #print(prob_speech_given_word)
            max_prob_pos=max(prob_speech_given_word,key=lambda x:x[1])
            l[idx]=max_prob_pos[0]
            idx+=1
        #print(l)
        return l

    #This is based on Prof David Crandall's code from the in-class activity. 
    # Instead of the 2 states of "R" and "Y", we will have 12 states, so the code to get the maximum will be different as the probabilities will be appended to a list from which the max will be calculated instead of an if-else loop in Prof. David's code                    
    def hmm_viterbi(self, sentence):

        for word in sentence:
            #print(sentence)
            viterbi_table={}
            which_table={}
            N=len(sentence)
    
            for s in self.s_list:
                viterbi_table[s]=[0]*N
                which_table[s]=[0]*N
            for s in self.s_list:
                if sentence[0] not in self.emission_probabilities[s]:
                    self.emission_probabilities[s][sentence[0]]=1e-5
                viterbi_table[s][0]=self.priors[s]*self.emission_probabilities[s][sentence[0]]
              
            for i in range(1,N):
                for s in self.s_list:
                    t1=[ (s0,viterbi_table[s0][i-1]*self.transition_probabilities[s0].get(s,1e-9)) for s0 in self.s_list]
                    #print(t1)
                    (which_table[s][i],viterbi_table[s][i])=max(t1, key=lambda x: x[1])
                    viterbi_table[s][i]=viterbi_table[s][i]*self.emission_probabilities[s][sentence[i]]



            #print(viterbi_table)
            viterbi_seq=[""]*len(sentence)
            m=0
            pos=[]
            for s in self.s_list:
                pos.append((s,viterbi_table[s][-1]))
            #print(pos)
            max_pos=max(pos,key=lambda x:x[1])
            viterbi_seq[N-1]=max_pos[0]
            #print(which_table)
            
            for i in range(len(sentence)-2,-1,-1):
                viterbi_seq[i]=which_table[viterbi_seq[i+1]][i+1]
            return viterbi_seq

    
    def get_gibbs_prob(self,sentence,sample):
        #print(sample)
        probability=0.0
        for i in range(len(sentence)-2):
            #If the word doesn't exist, then set probability to 1e-6
            # We could also add the word,speech in the dictionary, but then the dictionary would become extremely large 
            # Considering the fact that most samples will re-occur again, it's a safe bet to set it to 1e-6
            if sentence[i] in self.word_speech:
                ep=self.word_speech[sentence[i]].get(sample[i],1e-6)*self.priors[sample[i]]
            else:
                ep=-6
            #For First Word of Sentence, we will make use of the the initial distribution of Part's of Speech

            if i==0:
                tp=self.initial_pos[sample[i]]
                probability=probability+tp*ep
            #for second word , we will have just the one transition instead of 2
            if i==1:
                if sample[i] in self.transition_probabilities[sample[i-1]]:
                    tp=self.transition_probabilities[sample[i-1]][sample[i]]
                else:
                    tp=1e-6
                probability=probability+tp*ep
            #For all other words : consider 2 transitions from S1->S2 and S1->S3
            
            else:
                if sample[i+1] in self.transition_probabilities[sample[i]]:
                    tp1=self.transition_probabilities[sample[i]][sample[i+1]]
                else:
                    tp1=1e-6
                if sample[i+2] in self.transition_probabilities[sample[i+1]]: 
                    tp2=self.transition_probabilities[sample[i+1]][sample[i+2]]
                else:
                    tp2=1e-6
                if sample[i+2] in self.transition_probabilities_gibbs[sample[i]]:
                    tp3=self.transition_probabilities_gibbs[sample[i]][sample[i+2]]
                else:
                    tp3=1e-6
                if sentence[i+1] in self.word_speech:
                    ep2=self.word_speech[sentence[i+1]].get(sample[i+1],1e-6)*self.priors[sample[i+1]]
                else:
                    ep2=1e-6
                probability=probability+tp1*tp2*tp3*ep*ep2
        return probability

    def get_sample_string(self,sample):
        st=""
        for i in sample:
            st=st+i+"|"
        return st
    def complex_mcmc(self, sentence):
        #s: p(s1)*p(s2|s1)*p(s3|s1)*p(w|s1)
        N=len(sentence)
        result=['']*N
        #Get initial guess for POS from viterbi algorithm
        sample=['noun']*N
        #print(sample)
        gibbs=[]
        
        for i in range(700):
            
            for j in range(N):
                marginal_probabilities=[]       
                pos_list=[]
                for pos in self.s_list:
        
                    sample[j]=pos
                    #st=self.get_sample_string(sample)
                    gp=self.get_gibbs_prob(sentence,sample)
                    marginal_probabilities.append(gp)
                    pos_list.append(pos)
                #print(marginal_probabilities)
                #temp_sample=[(marginal_probabilities,pos_list)]
                sample[j]=pos_list[marginal_probabilities.index(max(marginal_probabilities))]
                gibbs.append(sample)
        
        for i in range(N):
            temp_result={}
            for j in range(len(gibbs)):
                if gibbs[j][i] in temp_result:
                    temp_result[gibbs[j][i]]=temp_result[gibbs[j][i]]+1
                else:
                    temp_result[gibbs[j][i]]=1
            result[i]=max(temp_result,key=lambda j:temp_result[j])
        return result

       
    
       
    


        

             
    # This solve() method is called by label.py, so you should keep the interface the
    #  same, but you can change the code itself. 
    # It should return a list of part-of-speech labelings of the sentence, one
    #  part of speech per word.
    #
    def solve(self, model, sentence):
        if model == "Simple":
            return self.simplified(sentence)
        elif model == "HMM":
            return self.hmm_viterbi(sentence)
        elif model == "Complex":
            return self.complex_mcmc(sentence)
        else:
            print("Unknown algo!")

