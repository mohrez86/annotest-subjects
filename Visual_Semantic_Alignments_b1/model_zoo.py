###############################################################################
# Author: Abhimanyu Banerjee
# Project: Visual Semantic Alignments
# Date Created: 5/8/2017
# 
# File Description: This script contains model definitions needed for the 
# experiments
###############################################################################

from __future__ import print_function
from keras.models import Model, Sequential
from keras.layers.core import Dense, Activation
from keras.layers import (LSTM, Input, RepeatVector, Lambda, Embedding, 
                            merge, concatenate)
from keras.layers.wrappers import TimeDistributed
from keras.layers.wrappers import Bidirectional  # repo_change
from keras.optimizers import RMSprop, Adam
import pdb

from model_utils import calc_score

from annotest import an_language as an


def text_model(vocab_size, max_len, embed_size, nb_hidden_states, batch_size, lr):
    
    input_seq = Input(batch_shape=(None, max_len))
    embedded = Embedding(vocab_size, embed_size, mask_zero=True)(input_seq)
    blstm = Bidirectional(LSTM(nb_hidden_states, return_sequences=True))(embedded)
    output_seq = TimeDistributed(Dense(vocab_size))(blstm)
    
    return output_seq


@an.arg("vocab_size", an.integers(min_value=900, max_value=1100))
@an.arg("max_len", an.integers(min_value=10, max_value=100))
@an.arg("embed_size", an.integers(min_value=200, max_value=400))
@an.arg("nb_hidden_states", an.sampled([512]))
@an.arg("nb_regs", an.sampled([10]))
def full_model(vocab_size, max_len, embed_size, nb_hidden_states, 
                nb_regs, nb_feats=4096, common_dim=300, batch_size=32, lr=0.01):

    text_input = Input(batch_shape=(None, max_len))
    # embedded = Embedding(vocab_size, embed_size, mask_zero=True)(input_seq)  # repo_change
    embedded = Embedding(vocab_size, embed_size, mask_zero=True)(text_input)  # repo_change
    blstm = Bidirectional(LSTM(nb_hidden_states, return_sequences=True))(embedded)
    text_out = TimeDistributed(Dense(common_dim))(blstm)

    vis_input = Input(batch_shape=(None, nb_regs, nb_feats))
    vis_out = Time_Distributed(Dense(common_dim))(vis_input)  # repo_bug
   
    score = Lambda(calc_score)([text_out, vis_out])

    return score
