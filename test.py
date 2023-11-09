from transformers import BertConfig
import sys,os
max_position_embeddings = sys.argv[1]
num_labels = 
vocab_size = 
bert_sequence_config =  BertConfig()
bert_sequence_config['vocab_size'] = vocab_size
bert_sequence_config['max_position_embeddings'] = max_position_embeddings
