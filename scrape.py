import pandas as pd
import numpy as np
import os
from re import sub
import wget
values='ABCDEFabcdef0123456789*'
val_to_int = dict((c, i) for i, c in enumerate(values))
maxlen=32
N_LANG=10
languages=["hi","bn","gu","kn","mr","or","ta","te","ml","pa"]
languages.sort()
global lang_map
ls=string.punctuation + '−।\u25AA\u0964'
global translate_table
translate_table=dict((ord(char),"") for char in ls)

triv_tokenizer_indic_pat=re.compile(r'(['+string.punctuation+r'\u0964\u0965'+r'])')
pat_num_seq=re.compile(r'([0-9]+ [,.:/] )+[0-9]+')

def tokenize_indic(text): 
    tok_str=triv_tokenizer_indic_pat.sub(r' \1 ',text.replace('\t',' '))

    s=re.sub(r'[ ]+',' ',tok_str).strip(' ')
    
    # do not tokenize numbers and dates
    new_s=''
   tokenize_indic(input_data) prev=0
    for m in pat_num_seq.finditer(s):
        start=m.start()
        end=m.end()
        if start>prev:
            new_s=new_s+s[prev:start]
            new_s=new_s+s[start:end].replace(' ','')
            prev=end
   
    new_s=new_s+s[prev:]
    s=new_s
    
    return s.split(' ')
    
def one_hot_encoded(data):
  integer_encoded=[]
  for i in range(len(data)):
    integer_encoded.append([val_to_int[char] for char in data[i]])
  one_hot_encoded = []   
  for i in integer_encoded:
    letter = np.zeros(len(values))
    for j in i:
      letter[j]=1
    one_hot_encoded.append(letter)
  while(len(one_hot_encoded)<maxlen):
    letter = np.zeros(len(values))
    one_hot_encoded.append(letter)
  return np.array(one_hot_encoded)

def generate_iscii_map():
  df=pd.read_csv('https://raw.githubusercontent.com/sonalgan/DeepLearning/master/iscii1.csv')
  lang_map=[]
  ls=dict()
  for lang in languages:
    ls=dict()
    for i,j in zip(df.iscii,df[lang]):
      if(j!=j):
        continue
      ls[j]=i
    lang_map.append(ls)
  return np.array(lang_map)


def process(data):
  iscii_encoded=[]
  data= sub(r"\d+","",data)
  data=re.sub(r"[a-zA-Z]+","",data)
  #print(data)
  for ch in data:
    #print(ch)
    for x in lang_map:
      y=list(x.keys())
      #print(y)
      if(ch in y):
          iscii_encoded.append(x[ch].capitalize())
          break
  return iscii_encoded

lang_map=generate_iscii_map()

def encode_labels(label):
    temp = np.zeros(N_LANG)
    i=languages.index(label)
    temp[i] = 1
    return temp

def main():
    
    
    
    X=list()
    Y=list()
    root=os.getcwd()
    url="https://hpedl.blob.core.windows.net/langdl/"

    for lang in languages:
        fp="{}.csv".format(lang)
        filename = wget.download(url+fp)
        print(filename)
        #!wget  -nc  {url+fp}
        filepath=os.path.join(root,fp)
        df=pd.read_csv(filepath,encoding='utf-8',header=None)
        for x,y in zip(df[0],df[1]):
            if(pd.isna(x)):
                  continue
            X.append(one_hot_encoded(process(x)))
            Y.append(encode_labels(y))
        os.remove(filepath)
        #!rm {filepath}
    del df
    dc={'words':X,'lang':Y}
    del X,Y
    df=pd.DataFrame(dc)
    del dc
    df=df.to_csv(os.path.join(root,'langdataset.csv'))
    return

if __name__ == "__main__":
    main()
