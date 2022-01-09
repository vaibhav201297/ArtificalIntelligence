#!/usr/bin/python
#
# Perform optical character recognition, usage:
#     python3 ./image2text.py train-image-file.png train-text.txt test-image-file.png
# 
# Authors: Abhijeet Sridhar Muralidharan - abhmura
# (based on skeleton code by D. Crandall, Oct 2020)
#

from PIL import Image
import copy
import heapq
import math
import re
import sys

CHARACTER_WIDTH = 14
CHARACTER_HEIGHT = 25

def load_letters(fname):
    im = Image.open(fname)
    px = im.load()
    (x_size, y_size) = im.size
    result = []
    for x_beg in range(0, int(x_size / CHARACTER_WIDTH) * CHARACTER_WIDTH, CHARACTER_WIDTH):
        # Removing initial "".join so that we get result in a better format
        result += [['*' if px[x, y] < 1 else ' ' for x in range(x_beg, x_beg + CHARACTER_WIDTH) for y in range(0, CHARACTER_HEIGHT)], ]
    return result


def load_training_letters(fname):
    TRAIN_LETTERS="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789(),.-!?\"' "
    letter_images = load_letters(fname)
    return { TRAIN_LETTERS[i]: letter_images[i] for i in range(0, len(TRAIN_LETTERS) ) }

# get number of alphabets
def get_alphabet_freq(dictionary):
    return sum(dictionary[alphabet] for alphabet in dictionary)

def get_transition_probabilities(transition_probabilities):
    for character in transition_probabilities:
        alphabet_freq = get_alphabet_freq(transition_probabilities[character])
        for alphabet in transition_probabilities[character]:
            transition_probabilities[character][alphabet] /= float(alphabet_freq)
    return transition_probabilities

# Use any file - bc.train in this case, to get the initial and transition probabilities
# this solution is inspired by https://github.com/Praneta-Paithankar/CSCI-B551-Elements-of-Artificial-Intelligence/blob/master/Assignment3/part2/ocr.py
def process_train_file(fname):
    
    initial_probabilities = {}
    transition_probabilities = {}
    
    file = open(fname, 'r');
    
    for sentence in file:
        
        alphabet_list = list(re.sub(r'[&|$|*|;|`|#|@|%|^|~|/|<|>|:|[|\]|{|}|+|=|_]', r'', " ".join([w for w in sentence.split()][0::2])))
        if alphabet_list:
            initial_probabilities[alphabet_list[0]] = initial_probabilities.get(alphabet_list[0], 0) + 1
            for alphabet in range(1, len(alphabet_list)):
                prev_alphabet = alphabet_list[alphabet - 1]
                cur_alphabet = alphabet_list[alphabet]
                
                if prev_alphabet in transition_probabilities:
                    val = transition_probabilities[prev_alphabet].get(cur_alphabet, 0)
                    transition_probabilities[prev_alphabet][cur_alphabet] = val + 1
                else:
                    this_transition_prob = {cur_alphabet: 1}
                    transition_probabilities[prev_alphabet] = this_transition_prob
    alphabet_freq_sum = get_alphabet_freq(initial_probabilities)
    for prob in initial_probabilities:
        initial_probabilities[prob] = float(initial_probabilities[prob]) / alphabet_freq_sum
    transition_probabilities = get_transition_probabilities(transition_probabilities)
    
    return initial_probabilities, transition_probabilities

# Calculate the emission probability
def get_emission_probabilities():
    emission_probabilities = {}
    test_empty_space = 0
    train_empty_space = 0
    
    for alphabet in train_letters:
        for star in train_letters[alphabet]:
            if star == '*':
                train_empty_space += 1
                
    for alphabet in test_letters:
        for star in alphabet:
            if star == '*':
                test_empty_space += 1
    
    for j in range(len(test_letters)):
        emission_probabilities[j] = {}
        for alphabet in train_letters:
            empty_count = 0
            filled_count = 0
            empty_unmatched = 0
            filled_unmatched = 0
            
            for i in range(len(test_letters[j])):
                if test_letters[j][i] == train_letters[alphabet][i]:
                    if train_letters[alphabet][i] == "*":
                        empty_count += 1
                    elif train_letters[alphabet][i] == " ":
                        filled_count += 1
                else:
                    if train_letters[alphabet][i] == "*":
                        empty_unmatched += 1
                    elif train_letters[alphabet][i] == " ":
                        filled_unmatched += 1
            
            # weights taken from the mentioned reference
            if test_empty_space / len(test_letters) > train_empty_space / len(train_letters):
                emission_probabilities[j][alphabet] = math.pow(0.8, empty_count) * math.pow(0.7,filled_count) * math.pow(0.3, empty_unmatched) * \
                                                                math.pow(0.2, filled_unmatched)
            else:
                emission_probabilities[j][alphabet] = math.pow(0.99, empty_count) * math.pow(0.7,filled_count) * math.pow(0.3, empty_unmatched) * \
                                                                math.pow(0.01, filled_unmatched)
    return emission_probabilities

# Simple bayes using only emission probabilities
def simplified(emission_probabilities):
    result = ""
    for alphabet in emission_probabilities:
        result += "".join(max(emission_probabilities[alphabet], key=lambda value: emission_probabilities[alphabet][value]))
    return result

# Viterbi
def viterbi(initial_probabilities, transition_probabilities, emission_probabilities):
    this_value = [-1] * 128
    last_value = [-1] * 128
    for n, _ in enumerate(test_letters):
        for _, alphabet in enumerate(train_letters):
            if n == 0:
                prob = -math.log(emission_probabilities[0][alphabet]) - math.log(
                    initial_probabilities.get(alphabet, math.pow(10, -8)))
                this_value[ord(alphabet)] = [prob, [alphabet]]
            else:
                min_heap = []
                for _, last_alphabet in enumerate(train_letters):
                    probability = -math.log(transition_probabilities.get(last_alphabet, {}).get(alphabet, math.pow(10, -8))) + last_value[ord(last_alphabet)][0]
                    min_heap.append([probability, last_value[ord(last_alphabet)][1] + [alphabet]])
                heapq.heapify(min_heap)
                highest_probability = heapq.heappop(min_heap)
                prob = highest_probability[0] - math.log(emission_probabilities[n][alphabet])
                this_value[ord(alphabet)] = [prob, highest_probability[1]]
        last_value = copy.deepcopy(this_value)
        this_value = [-1] * 128
    result = []
    for val in last_value:
        if val != -1:
            result.append(val)
    heapq.heapify(result)
    result = heapq.heappop(result)
    return "".join(result[1])

# main program
(train_img_fname, train_txt_fname, test_img_fname) = sys.argv[1:]
train_letters = load_training_letters(train_img_fname)
test_letters = load_letters(test_img_fname)
initial_probabilities, transition_probabilities = process_train_file(train_txt_fname)
emission_probabilities = get_emission_probabilities()
print("Simple: " + simplified(emission_probabilities))
print("HMM: " + viterbi(initial_probabilities, transition_probabilities, emission_probabilities))