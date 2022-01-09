# Assignment 3: Probability and Statistical Learning

## **Part 1 (Part-of-speech tagging - Vaibhav Vishwanath)** ##
The problem is Parts of Speech Tagging. Given a sentence, the task is to predict the parts of speech for the sentence.
We first train our model based on the training file in which the sentence along with the parts of speech is given.

In Model Training, we use the training file of corpus to generate 
<ol>
<li>Prior Probabilities : The probabilities of any word being a part of speech based on the total counts of corpus </li>
<li> The Initial Part of Speech Distribution: The distribution of probabilities for different parts of speech being the first word in a sentence </li>
<li> The Transition Probabilities : The transition from 1 part of speech to another based on the training data. We calculate 2 transitions : Speech1->Speech2 and Speech1->Speech3 </li>
<li> The Emission Probablities : The probability of seeing a certain observed variable(Word) given certain value for hidden variable(Part of Speech)</li>
</ol>

We have to implement 3 methods 
<ol><li> A Simple model : We just calculate the Part of Speech given the word based on just the current word </li>
<li> Viterbi Algorithm for HMM : In this we calculate the Parts of Speech based on the current observed state and the next state by taking into account the transition probabilities</li>
<li> A Complex MCMC using Gibbs Sampling : In this model, we consider the current state and the transition from the current to the next POS and the next-to-next POS. We use Gibbs sampling to generate samples of the POS distribution and then calculate the Posterior probabilties to get the most viable sample from distribution </li></ol>

<h3> Difficulties Faced </h3>
We have to take into consideration the scenario where the word in the testing data has not occured in the training data.<br/>
We also have to consider transitions that don't take place between 2 POS such as a '.' to 'adj'. 
<h4> References used </h4>
This assignment was a particularly difficult one and hence i had to use multiple references to solve them. I've cited the references in the code as well.
Link : <a href='https://github.com/sumeetmishra199189/Elements-of-AI/tree/master/Probability'>GitHub Repository</a><br/>
Prof. David's viterbi_sol.py  - The code used in the in-class activity of Viterbi has been modified to work for 12 states instead of 2 <br/>
I've also discussed strategy for solving the Gibbs Sampling code from my friend Shubhangi Mishra(shubmish). She helped me understand the working of Gibbs Sampling in this problem. 	

