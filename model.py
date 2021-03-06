# -*- coding: utf-8 -*-
"""Untitled6.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kT7vX6pr74U8lfdOSHK2XLVIa8nwcRgl
"""
'''
!pip install tensorflow-gpu

!nvidia-smi

!pip install --upgrade grpcio >> /dev/null

!pip install --upgrade grpcio==1.32.0 >> /dev/null

!pip install tqdm
!pip install bert-for-tf2

!pip install sentencepiece

!pip install scikit-learn
'''

# Commented out IPython magic to ensure Python compatibility.
import os
import math

from tqdm import tqdm

import pandas as pd
import numpy as np

import tensorflow as tf
from tensorflow import keras

import bert
from bert import BertModelLayer
from bert.loader import StockBertConfig,map_stock_config_to_params,load_stock_weights
from bert.tokenization.bert_tokenization import FullTokenizer

import seaborn as sns
from pylab import rcParams
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from matplotlib import rc


from sklearn.metrics import confusion_matrix , classification_report

# %matplotlib inline
# %config InlineBackend.figure_format = "retina"

sns.set(style="whitegrid",palette="muted",font_scale=1.2)
HAPPY_COLORS_PALLETE =["#01BEFE","#FFDD00","#FF7D00","#FF006D","#ADFF02","#8F00FF"]

sns.set_palette(sns.color_palette(HAPPY_COLORS_PALLETE))

rcParams["figure.figsize"]=12,8

RANDOM_SEED=42

np.random.seed(RANDOM_SEED)
tf.random.set_seed(RANDOM_SEED)

train = pd.read_csv("drive/MyDrive/data/dataset.csv",names=["article","group"])

for v,x in enumerate(train['article']):
    train['article'][v]=x.replace('\n','')



train = train.append(valid).reset_index(drop=True)

print(train.head())

print(train.shape)

print(train.emotion)

chart = sns.countplot(train.emotion,palette=HAPPY_COLORS_PALLETE)
plt.title("number of examples per intent")

!wget https://storage.googleapis.com/bert_models/2018_10_18/uncased_L-12_H-768_A-12.zip

!unzip uncased_L-12_H-768_A-12.zip

!ls

os.makedirs('model',exist_ok=True)

! mv uncased_L-12_H-768_A-12/ model

bert_model_name = 'uncased_L-12_H-768_A-12'
!ls

bert_ckpt_dir = os.path.join("model",bert_model_name)
bert_ckpt_file = os.path.join(bert_ckpt_dir,"bert_model.ckpt")
bert_config_file = os.path.join(bert_ckpt_dir,"bert_config.json")

class EmotionClassification:

  DATA_COLUMN="sentence"
  LABEL_COLUMN="emotion"


  def __init__(self,train,test,tokenizer:FullTokenizer,classes,max_seq_len=192):
    self.tokenizer = tokenizer
    self.max_seq_len = 0
    self.classes = classes

    ((self.train_x,self.train_y),(self.test_x,self.test_y))=map(self.prepare,[train,test])

    self.max_seq_len= min(max_seq_len,self.max_seq_len)

    self.train_x,self.test_x = map(self.pad,[self.train_x,self.test_x])

  def prepare(self,df):
    x,y=[],[]

    for _,row in tqdm(df.iterrows()):
      text,label = row[EmotionClassification.DATA_COLUMN],row[EmotionClassification.LABEL_COLUMN]

      tokens = self.tokenizer.tokenize(text)
      tokens = ["[CLS]"]+tokens+["[SEP]"]
        
      token_ids = self.tokenizer.convert_tokens_to_ids(tokens)

      self.max_seq_len= max(self.max_seq_len,len(token_ids))

      x.append(token_ids)
      y.append(self.classes.index(label))

    return np.array(x),np.array(y)


  def pad(self,ids):
    x=[]

    for input_ids in ids:
      cut_point = min(len(input_ids),self.max_seq_len-2)
      input_ids = input_ids[:cut_point]
      input_ids = input_ids + [0]*(self.max_seq_len-len(input_ids))
      x.append(input_ids)

    return np.array(x)

tokenizer = FullTokenizer(vocab_file=os.path.join(bert_ckpt_dir,"vocab.txt"))

def create_model(max_seq_len,bert_config_file,bert_ckpt_file):
  with tf.io.gfile.GFile(bert_config_file,"r") as reader:
    bc = StockBertConfig.from_json_string(reader.read())
    bert_params=map_stock_config_to_params(bc)
    bert_params.adapter_size = None
    bert = BertModelLayer.from_params(bert_params,name="bert")


    input_ids = keras.layers.Input(shape=(max_seq_len,),dtype="int32",name="input_ids")
    bert_output = bert(input_ids)

    print("bert_output",bert_output.shape)

    cls_out = keras.layers.Lambda(lambda seq: seq[:, 0, :])(bert_output)
    cls_out = keras.layers.Dropout(0.5)(cls_out)
    logits = keras.layers.Dense(units=768, activation="tanh")(cls_out)
    logits = keras.layers.Dropout(0.5)(logits)
    logits = keras.layers.Dense(units=len(classes), activation="softmax")(logits)

    model = keras.Model(inputs=input_ids, outputs=logits)
    model.build(input_shape=(None, max_seq_len))

    load_stock_weights(bert, bert_ckpt_file)
        
    return model

classes = train.emotion.unique().tolist()
data = EmotionClassification(train,test,tokenizer,classes,max_seq_len=128)

model = create_model(data.max_seq_len,bert_config_file,bert_ckpt_file)

print(model.summary())

model.compile(
  optimizer=keras.optimizers.Adam(1e-5),
  loss=keras.losses.SparseCategoricalCrossentropy(from_logits=True),
  metrics=[keras.metrics.SparseCategoricalAccuracy(name="acc")]
)

import datetime
log_dir = "log/emotion_detection/" + datetime.datetime.now().strftime("%Y%m%d-%H%M%s")
tensorboard_callback = keras.callbacks.TensorBoard(log_dir=log_dir)

history = model.fit(
  x=data.train_x, 
  y=data.train_y,
  validation_split=0.1,
  batch_size=16,
  shuffle=True,
  epochs=5,
  callbacks=[tensorboard_callback]
)

model.save_weights("drive/MyDrive/data/weights")

model.evaluate(data.test_x,data.test_y)

