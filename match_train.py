#! /usr/bin python
import sys
import os
import numpy as np
sys.path.append("./scripts/")
from scripts.match.dssm_bilstm import DSSM_biLSTM
from scripts.match.dssm import DSSM_CNN
from scripts.match.dssm_bilstm_attention import DSSM_biLSTM_attention
from data.match_data_loader import DataLoader
import argparse
parser = argparse.ArgumentParser()
parser.add_argument(
    "--conf_file",
    type=str,
    default="data/match_conf",
    help="conf_file containes sample files and labels")

parser.add_argument(
    "--w2v_path",
    type=str,
    default="/mnt/hgfs/share/pornCensor/query.skip.vec.win3",
    help="w2v file which provide w2v")
FLAGS, unparsed = parser.parse_known_args()
print ("unparsed: ", unparsed)
#conf_file = sys.argv[1]
#w2v_path = sys.argv[2]
conf_file = FLAGS.conf_file
w2v_path = FLAGS.w2v_path
loader = DataLoader()
loader.set_w2v(w2v_path)
#loader.save_dict("data/title_dict.json")
loader.build(conf_file)
train_data, train_label, test_data, test_label = loader.get_train_test()
print (train_label, test_label)
conf = { "title_features_dim": loader.word_vec_len,
         "article_features_dim": loader.word_vec_len,
         "vocab_size": len(loader.weights),
         "article_max_length": loader.article_len,
         "title_max_length": loader.title_len,
         "article_hidden_dims": 100,
         "title_hidden_dims": 100,
         "epochs": 100}

#model = DSSM_biLSTM(conf)
#model = DSSM_CNN(conf)
model = DSSM_biLSTM_attention(conf)
model.set_embedding(loader.get_weights())
model.build()
model.train(train_data, train_label, test_data, test_label)