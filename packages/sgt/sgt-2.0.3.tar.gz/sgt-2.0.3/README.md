# Sequence Graph Transform (SGT) &mdash; Sequence Embedding for Clustering, Classification, and Search

#### Maintained by: Chitta Ranjan 
Email: <cran2367@gmail.com>
| LinkedIn: [https://www.linkedin.com/in/chitta-ranjan-b0851911/](https://www.linkedin.com/in/chitta-ranjan-b0851911/)


The following will cover,

1. [SGT Class Definition](#sgt-class-def)
2. [Installation](#install-sgt)
3. [Test Examples](#installation-test-examples)
4. [Sequence Clustering Example](#sequence-clustering)
5. [Sequence Classification Example](#sequence-classification)
6. [Sequence Search Example](#sequence-search)
7. [SGT - Spark for Distributed Computing](#sgt-spark)


## <a name="sgt-class-def"></a> SGT Class Definition

Sequence Graph Transform (SGT) is a sequence embedding function. SGT extracts the short- and long-term sequence features and embeds them in a finite-dimensional feature space. The long and short term patterns embedded in SGT can be tuned without any increase in the computation."


```
class SGT():
    '''
    Compute embedding of a single or a collection of discrete item 
    sequences. A discrete item sequence is a sequence made from a set
    discrete elements, also known as alphabet set. For example,
    suppose the alphabet set is the set of roman letters, 
    {A, B, ..., Z}. This set is made of discrete elements. Examples of
    sequences from such a set are AABADDSA, UADSFJPFFFOIHOUGD, etc.
    Such sequence datasets are commonly found in online industry,
    for example, item purchase history, where the alphabet set is
    the set of all product items. Sequence datasets are abundant in
    bioinformatics as protein sequences.
    Using the embeddings created here, classification and clustering
    models can be built for sequence datasets.
    Read more in https://arxiv.org/pdf/1608.03533.pdf
    '''

    Parameters
    ----------
    Input:

    alphabets       Optional, except if mode is Spark. 
                    The set of alphabets that make up all 
                    the sequences in the dataset. If not passed, the
                    alphabet set is automatically computed as the 
                    unique set of elements that make all the sequences.
                    A list or 1d-array of the set of elements that make up the      
                    sequences. For example, np.array(["A", "B", "C"].
                    If mode is 'spark', the alphabets are necessary.

    kappa           Tuning parameter, kappa > 0, to change the extraction of 
                    long-term dependency. Higher the value the lesser
                    the long-term dependency captured in the embedding.
                    Typical values for kappa are 1, 5, 10.

    lengthsensitive Default false. This is set to true if the embedding of
                    should have the information of the length of the sequence.
                    If set to false then the embedding of two sequences with
                    similar pattern but different lengths will be the same.
                    lengthsensitive = false is similar to length-normalization.
                    
    flatten         Default True. If True the SGT embedding is flattened and returned as
                    a vector. Otherwise, it is returned as a matrix with the row and col
                    names same as the alphabets. The matrix form is used for            
                    interpretation purposes. Especially, to understand how the alphabets
                    are "related". Otherwise, for applying machine learning or deep
                    learning algorithms, the embedding vectors are required.
    
    mode            Choices in {'default', 'multiprocessing'}. Note: 'multiprocessing' 
                    mode requires pandas==1.0.3+ and pandarallel libraries.
    
    processors      Used if mode is 'multiprocessing'. By default, the 
                    number of processors used in multiprocessing is
                    number of available - 1.
    '''

    
    Attributes
    ----------
    def fit(sequence)
    
    Extract Sequence Graph Transform features using Algorithm-2 in https://arxiv.org/abs/1608.03533.
    Input:
    sequence        An array of discrete elements. For example,
                    np.array(["B","B","A","C","A","C","A","A","B","A"].
                    
    Output: 
    sgt embedding   sgt matrix or vector (depending on Flatten==False or True) of the sequence
    
    
    --
    def fit_transform(corpus)
    
    Extract SGT embeddings for all sequences in a corpus. It finds
    the alphabets encompassing all the sequences in the corpus, if not inputted. 
    However, if the mode is 'spark', then the alphabets list has to be
    explicitly given in Sgt object declaration.
    
    Input:
    corpus          A list of sequences. Each sequence is a list of alphabets.
    
    Output:
    sgt embedding of all sequences in the corpus.
    
    
    --
    def transform(corpus)
    
    Find SGT embeddings of a new data sample belonging to the same population
    of the corpus that was fitted initially.
```

## <a name="install-sgt"></a> Install SGT

Install SGT in Python by running,

```$ pip install sgt```


```python
import sgt
sgt.__version__
from sgt import SGT

```




    '2.0.0'





```python
# -*- coding: utf-8 -*-
# Authors: Chitta Ranjan <cran2367@gmail.com>
#
# License: BSD 3 clause
```


## <a name="installation-test-examples"></a> Installation Test Examples

In the following, there are a few test examples to verify the installation.


```python
# Learning a sgt embedding as a matrix with 
# rows and columns as the sequence alphabets. 
# This embedding shows the relationship between 
# the alphabets. The higher the value the 
# stronger the relationship.

sgt = SGT(flatten=False)
sequence = np.array(["B","B","A","C","A","C","A","A","B","A"])
sgt.fit(sequence)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>A</th>
      <th>B</th>
      <th>C</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>A</th>
      <td>0.090616</td>
      <td>0.131002</td>
      <td>0.261849</td>
    </tr>
    <tr>
      <th>B</th>
      <td>0.086569</td>
      <td>0.123042</td>
      <td>0.052544</td>
    </tr>
    <tr>
      <th>C</th>
      <td>0.137142</td>
      <td>0.028263</td>
      <td>0.135335</td>
    </tr>
  </tbody>
</table>
</div>




```python
# SGT embedding to a vector. The vector
# embedding is useful for directly applying
# a machine learning algorithm.

sgt = SGT(flatten=True)
sequence = np.array(["B","B","A","C","A","C","A","A","B","A"])
sgt.fit(sequence)
```




    (A, A)    0.090616
    (A, B)    0.131002
    (A, C)    0.261849
    (B, A)    0.086569
    (B, B)    0.123042
    (B, C)    0.052544
    (C, A)    0.137142
    (C, B)    0.028263
    (C, C)    0.135335
    dtype: float64




```python
'''
SGT embedding on a corpus of sequences.
Test the two processing modes within the
SGT class: 'default', 'multiprocessing'.

'''

# A sample corpus of two sequences.
corpus = pd.DataFrame([[1, ["B","B","A","C","A","C","A","A","B","A"]], 
                       [2, ["C", "Z", "Z", "Z", "D"]]], 
                      columns=['id', 'sequence'])
corpus
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>sequence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1</td>
      <td>[B, B, A, C, A, C, A, A, B, A]</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2</td>
      <td>[C, Z, Z, Z, D]</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Learning the sgt embeddings as vector for
# all sequences in a corpus.
# mode: 'default'
sgt = SGT(kappa=1, 
          flatten=True, 
          lengthsensitive=False, 
          mode='default')
sgt.fit_transform(corpus)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>(A, A)</th>
      <th>(A, B)</th>
      <th>(A, C)</th>
      <th>(A, D)</th>
      <th>(A, Z)</th>
      <th>(B, A)</th>
      <th>(B, B)</th>
      <th>(B, C)</th>
      <th>(B, D)</th>
      <th>...</th>
      <th>(D, A)</th>
      <th>(D, B)</th>
      <th>(D, C)</th>
      <th>(D, D)</th>
      <th>(D, Z)</th>
      <th>(Z, A)</th>
      <th>(Z, B)</th>
      <th>(Z, C)</th>
      <th>(Z, D)</th>
      <th>(Z, Z)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.0</td>
      <td>0.090616</td>
      <td>0.131002</td>
      <td>0.261849</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.086569</td>
      <td>0.123042</td>
      <td>0.052544</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.184334</td>
      <td>0.290365</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 26 columns</p>
</div>




```python
# Learning the sgt embeddings as vector for
# all sequences in a corpus.
# mode: 'multiprocessing'

import pandarallel  # required library for multiprocessing

sgt = SGT(kappa=1, 
          flatten=True, 
          lengthsensitive=False,
          mode='multiprocessing')

sgt.fit_transform(corpus)
```

    INFO: Pandarallel will run on 7 workers.
    INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>(A, A)</th>
      <th>(A, B)</th>
      <th>(A, C)</th>
      <th>(A, D)</th>
      <th>(A, Z)</th>
      <th>(B, A)</th>
      <th>(B, B)</th>
      <th>(B, C)</th>
      <th>(B, D)</th>
      <th>...</th>
      <th>(D, A)</th>
      <th>(D, B)</th>
      <th>(D, C)</th>
      <th>(D, D)</th>
      <th>(D, Z)</th>
      <th>(Z, A)</th>
      <th>(Z, B)</th>
      <th>(Z, C)</th>
      <th>(Z, D)</th>
      <th>(Z, Z)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>1.0</td>
      <td>0.090616</td>
      <td>0.131002</td>
      <td>0.261849</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.086569</td>
      <td>0.123042</td>
      <td>0.052544</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>...</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.0</td>
      <td>0.184334</td>
      <td>0.290365</td>
    </tr>
  </tbody>
</table>
<p>2 rows × 26 columns</p>
</div>

## Load Libraries for Illustrative Examples


```python
from sgt import SGT

import numpy as np
import pandas as pd
from itertools import chain
from itertools import product as iterproduct
import warnings

import pickle

########
from sklearn.preprocessing import LabelEncoder
import tensorflow as tf
from keras.datasets import imdb
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from tensorflow.keras.layers import Dropout
from tensorflow.keras.layers import Activation
from tensorflow.keras.layers import Flatten
from tensorflow.keras.layers import Embedding
from tensorflow.keras.preprocessing import sequence

from sklearn.model_selection import train_test_split
from sklearn.model_selection import KFold
from sklearn.model_selection import StratifiedKFold
import sklearn.metrics
import time

from sklearn.decomposition import PCA
from sklearn.cluster import KMeans

import matplotlib.pyplot as plt
%matplotlib inline

np.random.seed(7) # fix random seed for reproducibility

# from sgt import Sgt
```


## <a name="sequence-clustering"></a> Sequence Clustering

A form of unsupervised learning from sequences is clustering. For example, in 

- user weblogs sequences: clustering the weblogs segments users into groups with similar browsing behavior. This helps in targeted marketing, anomaly detection, and other web customizations.

- protein sequences: clustering proteins with similar structures help researchers study the commonalities between species. It also helps in faster search in some search algorithms.

In the following, clustering on a protein sequence dataset will be shown.



### Protein Sequence Clustering

The data used here is taken from www.uniprot.org. This is a public database for proteins. The data contains the protein sequences and their functions.


```python
# Loading data
corpus = pd.read_csv('data/protein_classification.csv')

# Data preprocessing
corpus = corpus.loc[:,['Entry','Sequence']]
corpus.columns = ['id', 'sequence']
corpus['sequence'] = corpus['sequence'].map(list)
corpus
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>sequence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M7MCX3</td>
      <td>[M, E, I, E, K, T, N, R, M, N, A, L, F, E, F, ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>K6PL84</td>
      <td>[M, E, I, E, K, N, Y, R, M, N, S, L, F, E, F, ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R4W5V3</td>
      <td>[M, E, I, E, K, T, N, R, M, N, A, L, F, E, F, ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T2A126</td>
      <td>[M, E, I, E, K, T, N, R, M, N, A, L, F, E, F, ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>L0SHD5</td>
      <td>[M, E, I, E, K, T, N, R, M, N, A, L, F, E, F, ...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2107</th>
      <td>A0A081R612</td>
      <td>[M, M, N, M, Q, N, M, M, R, Q, A, Q, K, L, Q, ...</td>
    </tr>
    <tr>
      <th>2108</th>
      <td>A0A081QQM2</td>
      <td>[M, M, N, M, Q, N, M, M, R, Q, A, Q, K, L, Q, ...</td>
    </tr>
    <tr>
      <th>2109</th>
      <td>J1A517</td>
      <td>[M, M, R, Q, A, Q, K, L, Q, K, Q, M, E, Q, S, ...</td>
    </tr>
    <tr>
      <th>2110</th>
      <td>F5U1T6</td>
      <td>[M, M, N, M, Q, S, M, M, K, Q, A, Q, K, L, Q, ...</td>
    </tr>
    <tr>
      <th>2111</th>
      <td>J3A2T7</td>
      <td>[M, M, N, M, Q, N, M, M, K, Q, A, Q, K, L, Q, ...</td>
    </tr>
  </tbody>
</table>
<p>2112 rows × 2 columns</p>
</div>




```python
%%time
# Compute SGT embeddings
sgt_ = SGT(kappa=1, 
           lengthsensitive=False, 
           mode='multiprocessing')
sgtembedding_df = sgt_.fit_transform(corpus)
```

    INFO: Pandarallel will run on 7 workers.
    INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.
    CPU times: user 324 ms, sys: 68 ms, total: 392 ms
    Wall time: 9.02 s



```python
sgtembedding_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>(A, A)</th>
      <th>(A, C)</th>
      <th>(A, D)</th>
      <th>(A, E)</th>
      <th>(A, F)</th>
      <th>(A, G)</th>
      <th>(A, H)</th>
      <th>(A, I)</th>
      <th>(A, K)</th>
      <th>...</th>
      <th>(Y, M)</th>
      <th>(Y, N)</th>
      <th>(Y, P)</th>
      <th>(Y, Q)</th>
      <th>(Y, R)</th>
      <th>(Y, S)</th>
      <th>(Y, T)</th>
      <th>(Y, V)</th>
      <th>(Y, W)</th>
      <th>(Y, Y)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>M7MCX3</td>
      <td>0.020180</td>
      <td>0.0</td>
      <td>0.009635</td>
      <td>0.013529</td>
      <td>0.009360</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.002226</td>
      <td>0.000379</td>
      <td>...</td>
      <td>0.009196</td>
      <td>0.007964</td>
      <td>0.036788</td>
      <td>0.000195</td>
      <td>0.001513</td>
      <td>0.020665</td>
      <td>0.000542</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.010419</td>
    </tr>
    <tr>
      <th>1</th>
      <td>K6PL84</td>
      <td>0.001604</td>
      <td>0.0</td>
      <td>0.012637</td>
      <td>0.006323</td>
      <td>0.006224</td>
      <td>0.004819</td>
      <td>3.560677e-03</td>
      <td>0.001124</td>
      <td>0.012136</td>
      <td>...</td>
      <td>0.135335</td>
      <td>0.006568</td>
      <td>0.038901</td>
      <td>0.011298</td>
      <td>0.012578</td>
      <td>0.009913</td>
      <td>0.001079</td>
      <td>0.000023</td>
      <td>0.0</td>
      <td>0.007728</td>
    </tr>
    <tr>
      <th>2</th>
      <td>R4W5V3</td>
      <td>0.012448</td>
      <td>0.0</td>
      <td>0.008408</td>
      <td>0.016363</td>
      <td>0.027469</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.004249</td>
      <td>0.013013</td>
      <td>...</td>
      <td>0.008114</td>
      <td>0.007128</td>
      <td>0.000000</td>
      <td>0.000203</td>
      <td>0.001757</td>
      <td>0.022736</td>
      <td>0.000249</td>
      <td>0.012652</td>
      <td>0.0</td>
      <td>0.008533</td>
    </tr>
    <tr>
      <th>3</th>
      <td>T2A126</td>
      <td>0.010545</td>
      <td>0.0</td>
      <td>0.012560</td>
      <td>0.014212</td>
      <td>0.013728</td>
      <td>0.000000</td>
      <td>2.944887e-10</td>
      <td>0.007223</td>
      <td>0.000309</td>
      <td>...</td>
      <td>0.000325</td>
      <td>0.009669</td>
      <td>0.000000</td>
      <td>0.003182</td>
      <td>0.001904</td>
      <td>0.015607</td>
      <td>0.000577</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.008648</td>
    </tr>
    <tr>
      <th>4</th>
      <td>L0SHD5</td>
      <td>0.020180</td>
      <td>0.0</td>
      <td>0.008628</td>
      <td>0.015033</td>
      <td>0.009360</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.002226</td>
      <td>0.000379</td>
      <td>...</td>
      <td>0.009196</td>
      <td>0.007964</td>
      <td>0.036788</td>
      <td>0.000195</td>
      <td>0.001513</td>
      <td>0.020665</td>
      <td>0.000542</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.010419</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>2107</th>
      <td>A0A081R612</td>
      <td>0.014805</td>
      <td>0.0</td>
      <td>0.004159</td>
      <td>0.017541</td>
      <td>0.012701</td>
      <td>0.013099</td>
      <td>0.000000e+00</td>
      <td>0.017043</td>
      <td>0.004732</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2108</th>
      <td>A0A081QQM2</td>
      <td>0.010774</td>
      <td>0.0</td>
      <td>0.004283</td>
      <td>0.014732</td>
      <td>0.014340</td>
      <td>0.014846</td>
      <td>0.000000e+00</td>
      <td>0.016806</td>
      <td>0.005406</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2109</th>
      <td>J1A517</td>
      <td>0.010774</td>
      <td>0.0</td>
      <td>0.004283</td>
      <td>0.014732</td>
      <td>0.014340</td>
      <td>0.014846</td>
      <td>0.000000e+00</td>
      <td>0.014500</td>
      <td>0.005406</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2110</th>
      <td>F5U1T6</td>
      <td>0.015209</td>
      <td>0.0</td>
      <td>0.005175</td>
      <td>0.023888</td>
      <td>0.011410</td>
      <td>0.011510</td>
      <td>0.000000e+00</td>
      <td>0.021145</td>
      <td>0.009280</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>2111</th>
      <td>J3A2T7</td>
      <td>0.005240</td>
      <td>0.0</td>
      <td>0.012301</td>
      <td>0.013178</td>
      <td>0.014744</td>
      <td>0.014705</td>
      <td>0.000000e+00</td>
      <td>0.000981</td>
      <td>0.007957</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
<p>2112 rows × 401 columns</p>
</div>




```python
# Set the id column as the dataframe index
sgtembedding_df = sgtembedding_df.set_index('id')
sgtembedding_df
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>(A, A)</th>
      <th>(A, C)</th>
      <th>(A, D)</th>
      <th>(A, E)</th>
      <th>(A, F)</th>
      <th>(A, G)</th>
      <th>(A, H)</th>
      <th>(A, I)</th>
      <th>(A, K)</th>
      <th>(A, L)</th>
      <th>...</th>
      <th>(Y, M)</th>
      <th>(Y, N)</th>
      <th>(Y, P)</th>
      <th>(Y, Q)</th>
      <th>(Y, R)</th>
      <th>(Y, S)</th>
      <th>(Y, T)</th>
      <th>(Y, V)</th>
      <th>(Y, W)</th>
      <th>(Y, Y)</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>M7MCX3</th>
      <td>0.020180</td>
      <td>0.0</td>
      <td>0.009635</td>
      <td>0.013529</td>
      <td>0.009360</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.002226</td>
      <td>0.000379</td>
      <td>0.021703</td>
      <td>...</td>
      <td>0.009196</td>
      <td>0.007964</td>
      <td>0.036788</td>
      <td>0.000195</td>
      <td>0.001513</td>
      <td>0.020665</td>
      <td>0.000542</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.010419</td>
    </tr>
    <tr>
      <th>K6PL84</th>
      <td>0.001604</td>
      <td>0.0</td>
      <td>0.012637</td>
      <td>0.006323</td>
      <td>0.006224</td>
      <td>0.004819</td>
      <td>3.560677e-03</td>
      <td>0.001124</td>
      <td>0.012136</td>
      <td>0.018427</td>
      <td>...</td>
      <td>0.135335</td>
      <td>0.006568</td>
      <td>0.038901</td>
      <td>0.011298</td>
      <td>0.012578</td>
      <td>0.009913</td>
      <td>0.001079</td>
      <td>0.000023</td>
      <td>0.0</td>
      <td>0.007728</td>
    </tr>
    <tr>
      <th>R4W5V3</th>
      <td>0.012448</td>
      <td>0.0</td>
      <td>0.008408</td>
      <td>0.016363</td>
      <td>0.027469</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.004249</td>
      <td>0.013013</td>
      <td>0.031118</td>
      <td>...</td>
      <td>0.008114</td>
      <td>0.007128</td>
      <td>0.000000</td>
      <td>0.000203</td>
      <td>0.001757</td>
      <td>0.022736</td>
      <td>0.000249</td>
      <td>0.012652</td>
      <td>0.0</td>
      <td>0.008533</td>
    </tr>
    <tr>
      <th>T2A126</th>
      <td>0.010545</td>
      <td>0.0</td>
      <td>0.012560</td>
      <td>0.014212</td>
      <td>0.013728</td>
      <td>0.000000</td>
      <td>2.944887e-10</td>
      <td>0.007223</td>
      <td>0.000309</td>
      <td>0.028531</td>
      <td>...</td>
      <td>0.000325</td>
      <td>0.009669</td>
      <td>0.000000</td>
      <td>0.003182</td>
      <td>0.001904</td>
      <td>0.015607</td>
      <td>0.000577</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.008648</td>
    </tr>
    <tr>
      <th>L0SHD5</th>
      <td>0.020180</td>
      <td>0.0</td>
      <td>0.008628</td>
      <td>0.015033</td>
      <td>0.009360</td>
      <td>0.003205</td>
      <td>2.944887e-10</td>
      <td>0.002226</td>
      <td>0.000379</td>
      <td>0.021703</td>
      <td>...</td>
      <td>0.009196</td>
      <td>0.007964</td>
      <td>0.036788</td>
      <td>0.000195</td>
      <td>0.001513</td>
      <td>0.020665</td>
      <td>0.000542</td>
      <td>0.007479</td>
      <td>0.0</td>
      <td>0.010419</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>A0A081R612</th>
      <td>0.014805</td>
      <td>0.0</td>
      <td>0.004159</td>
      <td>0.017541</td>
      <td>0.012701</td>
      <td>0.013099</td>
      <td>0.000000e+00</td>
      <td>0.017043</td>
      <td>0.004732</td>
      <td>0.014904</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>A0A081QQM2</th>
      <td>0.010774</td>
      <td>0.0</td>
      <td>0.004283</td>
      <td>0.014732</td>
      <td>0.014340</td>
      <td>0.014846</td>
      <td>0.000000e+00</td>
      <td>0.016806</td>
      <td>0.005406</td>
      <td>0.014083</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>J1A517</th>
      <td>0.010774</td>
      <td>0.0</td>
      <td>0.004283</td>
      <td>0.014732</td>
      <td>0.014340</td>
      <td>0.014846</td>
      <td>0.000000e+00</td>
      <td>0.014500</td>
      <td>0.005406</td>
      <td>0.014083</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>F5U1T6</th>
      <td>0.015209</td>
      <td>0.0</td>
      <td>0.005175</td>
      <td>0.023888</td>
      <td>0.011410</td>
      <td>0.011510</td>
      <td>0.000000e+00</td>
      <td>0.021145</td>
      <td>0.009280</td>
      <td>0.017466</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
    <tr>
      <th>J3A2T7</th>
      <td>0.005240</td>
      <td>0.0</td>
      <td>0.012301</td>
      <td>0.013178</td>
      <td>0.014744</td>
      <td>0.014705</td>
      <td>0.000000e+00</td>
      <td>0.000981</td>
      <td>0.007957</td>
      <td>0.017112</td>
      <td>...</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.0</td>
      <td>0.000000</td>
    </tr>
  </tbody>
</table>
<p>2112 rows × 400 columns</p>
</div>



We perform PCA on the sequence embeddings and then do kmeans clustering.


```python
pca = PCA(n_components=2)
pca.fit(sgtembedding_df)

X=pca.transform(sgtembedding_df)

print(np.sum(pca.explained_variance_ratio_))
df = pd.DataFrame(data=X, columns=['x1', 'x2'])
df.head()
```

    0.6432744907364981





<div>

<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>x1</th>
      <th>x2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0.384913</td>
      <td>-0.269873</td>
    </tr>
    <tr>
      <th>1</th>
      <td>0.022764</td>
      <td>0.135995</td>
    </tr>
    <tr>
      <th>2</th>
      <td>0.177792</td>
      <td>-0.172454</td>
    </tr>
    <tr>
      <th>3</th>
      <td>0.168074</td>
      <td>-0.147334</td>
    </tr>
    <tr>
      <th>4</th>
      <td>0.383616</td>
      <td>-0.271163</td>
    </tr>
  </tbody>
</table>
</div>




```python
kmeans = KMeans(n_clusters=3, max_iter =300)
kmeans.fit(df)

labels = kmeans.predict(df)
centroids = kmeans.cluster_centers_

fig = plt.figure(figsize=(5, 5))
colmap = {1: 'r', 2: 'g', 3: 'b'}
colors = list(map(lambda x: colmap[x+1], labels))
plt.scatter(df['x1'], df['x2'], color=colors, alpha=0.5, edgecolor=colors)
```




    <matplotlib.collections.PathCollection at 0x14c5a77f0>




![png](output_23_1.png)


## <a name="sequence-classification"></a> Sequence Classification using Deep Learning in TensorFlow

The protein data set used above is also labeled. The labels represent the protein functions. Similarly, there are other labeled sequence data sets. For example, DARPA shared an intrusion weblog data set. It contains weblog sequences with positive labels if the log represents a network intrusion.

In such problems supervised learning is employed. Classification is a supervised learning we will demonstrate here.

### Protein Sequence Classification

The data set is taken from https://www.uniprot.org . The protein sequences in the data set have one of the two functions,
- Binds to DNA and alters its conformation. May be involved in regulation of gene expression, nucleoid organization and DNA protection.
- Might take part in the signal recognition particle (SRP) pathway. This is inferred from the conservation of its genetic proximity to ftsY/ffh. May be a regulatory protein.

There are a total of 2113 samples. The sequence lengths vary between 100-700.


```python
# Loading data
data = pd.read_csv('data/protein_classification.csv')


# Data preprocessing
y = data['Function [CC]']
encoder = LabelEncoder()
encoder.fit(y)
encoded_y = encoder.transform(y)

corpus = data.loc[:,['Entry','Sequence']]
corpus.columns = ['id', 'sequence']
corpus['sequence'] = corpus['sequence'].map(list)
```

#### Sequence embeddings


```python
# Sequence embedding
sgt_ = SGT(kappa=1, 
           lengthsensitive=False, 
           mode='multiprocessing')
sgtembedding_df = sgt_.fit_transform(corpus)
X = sgtembedding_df.set_index('id')
```

    INFO: Pandarallel will run on 7 workers.
    INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.


We will perform a 10-fold cross-validation to measure the performance of the classification model.


```python
kfold = 10
X = X
y = encoded_y

random_state = 1

test_F1 = np.zeros(kfold)
skf = KFold(n_splits = kfold, shuffle = True, random_state = random_state)
k = 0
epochs = 50
batch_size = 128

for train_index, test_index in skf.split(X, y):
    X_train, X_test = X.iloc[train_index], X.iloc[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    model = Sequential()
    model.add(Dense(64, input_shape = (X_train.shape[1],))) 
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(32))
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    model.fit(X_train, y_train ,batch_size=batch_size, epochs=epochs, verbose=0)
    
    y_pred = model.predict_proba(X_test).round().astype(int)
    y_train_pred = model.predict_proba(X_train).round().astype(int)

    test_F1[k] = sklearn.metrics.f1_score(y_test, y_pred)
    k+=1
    
print ('Average f1 score', np.mean(test_F1))
```

    Average f1 score 1.0


### Weblog Classification for Intrusion Detection

This data sample is taken from https://www.ll.mit.edu/r-d/datasets/1998-darpa-intrusion-detection-evaluation-dataset. 
This is a network intrusion data containing audit logs and any attack as a positive label. Since, network intrusion is a rare event, the data is unbalanced. Here we will,
- build a sequence classification model to predict a network intrusion.

Each sequence contains in the data is a series of activity, for example, {login, password}. The _alphabets_ in the input data sequences are already encoded into integers. The original sequences data file is also present in the `/data` directory.


```python
# Loading data
data = pd.read_csv('data/darpa_data.csv')
data.columns
```




    Index(['timeduration', 'seqlen', 'seq', 'class'], dtype='object')




```python
data['id'] = data.index
```


```python
# Data preprocessing
y = data['class']
encoder = LabelEncoder()
encoder.fit(y)
encoded_y = encoder.transform(y)

corpus = data.loc[:,['id','seq']]
corpus.columns = ['id', 'sequence']
corpus['sequence'] = corpus['sequence'].map(list)
```

#### Sequence embeddings
In this data, the sequence embeddings should be **length-sensitive**. 

The lengths are important here because sequences with similar patterns but different lengths can have different labels. Consider a simple example of two sessions: `{login, pswd, login, pswd,...}` and `{login, pswd,...(repeated several times)..., login, pswd}`. 

While the first session can be a regular user mistyping the password once, the other session is possibly an attack to guess the password. Thus, the sequence lengths are as important as the patterns.

Therefore, `lengthsensitive=True` is used here.


```python
# Sequence embedding
sgt_ = SGT(kappa=5, 
           lengthsensitive=True, 
           mode='multiprocessing')
sgtembedding_df = sgt_.fit_transform(corpus)
sgtembedding_df = sgtembedding_df.set_index('id')
sgtembedding_df
```

    INFO: Pandarallel will run on 7 workers.
    INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.





<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>(0, 0)</th>
      <th>(0, 1)</th>
      <th>(0, 2)</th>
      <th>(0, 3)</th>
      <th>(0, 4)</th>
      <th>(0, 5)</th>
      <th>(0, 6)</th>
      <th>(0, 7)</th>
      <th>(0, 8)</th>
      <th>(0, 9)</th>
      <th>...</th>
      <th>(~, 1)</th>
      <th>(~, 2)</th>
      <th>(~, 3)</th>
      <th>(~, 4)</th>
      <th>(~, 5)</th>
      <th>(~, 6)</th>
      <th>(~, 7)</th>
      <th>(~, 8)</th>
      <th>(~, 9)</th>
      <th>(~, ~)</th>
    </tr>
    <tr>
      <th>id</th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0.0</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.485034</td>
      <td>0.486999</td>
      <td>0.485802</td>
      <td>0.483097</td>
      <td>0.483956</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.178609</td>
    </tr>
    <tr>
      <th>1.0</th>
      <td>0.000000</td>
      <td>0.025622</td>
      <td>0.228156</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>1.310714e-09</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.447620</td>
      <td>0.452097</td>
      <td>0.464568</td>
      <td>0.367296</td>
      <td>0.525141</td>
      <td>0.455018</td>
      <td>0.374364</td>
      <td>0.414081</td>
      <td>0.549981</td>
      <td>0.172479</td>
    </tr>
    <tr>
      <th>2.0</th>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.525605</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.193359</td>
      <td>0.071469</td>
    </tr>
    <tr>
      <th>3.0</th>
      <td>0.077999</td>
      <td>0.208974</td>
      <td>0.230338</td>
      <td>1.830519e-01</td>
      <td>1.200926e-17</td>
      <td>1.696880e-01</td>
      <td>0.093646</td>
      <td>7.985870e-02</td>
      <td>2.896813e-05</td>
      <td>3.701710e-05</td>
      <td>...</td>
      <td>0.474072</td>
      <td>0.468353</td>
      <td>0.463594</td>
      <td>0.177507</td>
      <td>0.551270</td>
      <td>0.418652</td>
      <td>0.309652</td>
      <td>0.384657</td>
      <td>0.378225</td>
      <td>0.170362</td>
    </tr>
    <tr>
      <th>4.0</th>
      <td>0.000000</td>
      <td>0.023695</td>
      <td>0.217819</td>
      <td>2.188276e-33</td>
      <td>0.000000e+00</td>
      <td>6.075992e-11</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>5.681668e-39</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.464120</td>
      <td>0.468229</td>
      <td>0.452170</td>
      <td>0.000000</td>
      <td>0.501242</td>
      <td>0.000000</td>
      <td>0.300534</td>
      <td>0.161961</td>
      <td>0.000000</td>
      <td>0.167082</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>106.0</th>
      <td>0.000000</td>
      <td>0.024495</td>
      <td>0.219929</td>
      <td>2.035190e-17</td>
      <td>1.073271e-18</td>
      <td>5.656994e-11</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>5.047380e-29</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.502213</td>
      <td>0.544343</td>
      <td>0.477281</td>
      <td>0.175901</td>
      <td>0.461103</td>
      <td>0.000000</td>
      <td>0.000000</td>
      <td>0.162796</td>
      <td>0.000000</td>
      <td>0.167687</td>
    </tr>
    <tr>
      <th>107.0</th>
      <td>0.110422</td>
      <td>0.227478</td>
      <td>0.217549</td>
      <td>1.723963e-01</td>
      <td>1.033292e-14</td>
      <td>3.896725e-07</td>
      <td>0.083685</td>
      <td>2.940589e-08</td>
      <td>8.864072e-02</td>
      <td>4.813990e-29</td>
      <td>...</td>
      <td>0.490398</td>
      <td>0.522016</td>
      <td>0.466808</td>
      <td>0.470603</td>
      <td>0.479795</td>
      <td>0.480057</td>
      <td>0.194888</td>
      <td>0.172397</td>
      <td>0.164873</td>
      <td>0.172271</td>
    </tr>
    <tr>
      <th>108.0</th>
      <td>0.005646</td>
      <td>0.202424</td>
      <td>0.196786</td>
      <td>2.281242e-01</td>
      <td>1.133936e-01</td>
      <td>1.862098e-01</td>
      <td>0.000000</td>
      <td>1.212869e-01</td>
      <td>9.180520e-08</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.432834</td>
      <td>0.434953</td>
      <td>0.439615</td>
      <td>0.390864</td>
      <td>0.481764</td>
      <td>0.600875</td>
      <td>0.166766</td>
      <td>0.165368</td>
      <td>0.000000</td>
      <td>0.171729</td>
    </tr>
    <tr>
      <th>109.0</th>
      <td>0.000000</td>
      <td>0.025616</td>
      <td>0.238176</td>
      <td>3.889176e-55</td>
      <td>1.332427e-60</td>
      <td>1.408003e-09</td>
      <td>0.000000</td>
      <td>9.845377e-60</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.421318</td>
      <td>0.439985</td>
      <td>0.467953</td>
      <td>0.440951</td>
      <td>0.527165</td>
      <td>0.864717</td>
      <td>0.407155</td>
      <td>0.399335</td>
      <td>0.251304</td>
      <td>0.171885</td>
    </tr>
    <tr>
      <th>110.0</th>
      <td>0.000000</td>
      <td>0.022868</td>
      <td>0.203513</td>
      <td>9.273472e-64</td>
      <td>0.000000e+00</td>
      <td>1.240870e-09</td>
      <td>0.000000</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>0.000000e+00</td>
      <td>...</td>
      <td>0.478090</td>
      <td>0.454871</td>
      <td>0.459109</td>
      <td>0.000000</td>
      <td>0.490534</td>
      <td>0.370357</td>
      <td>0.000000</td>
      <td>0.162997</td>
      <td>0.000000</td>
      <td>0.162089</td>
    </tr>
  </tbody>
</table>
<p>111 rows × 121 columns</p>
</div>



#### Applying PCA on the embeddings
The embeddings are sparse and high-dimensional. PCA is, therefore, applied for dimension reduction.


```python
from sklearn.decomposition import PCA
pca = PCA(n_components=35)
pca.fit(sgtembedding_df)
X = pca.transform(sgtembedding_df)
print(np.sum(pca.explained_variance_ratio_))
```

    0.9962446146783123


#### Building a Multi-Layer Perceptron Classifier
The PCA transforms of the embeddings are used directly as inputs to an MLP classifier.


```python
kfold = 3
random_state = 11

X = X
y = encoded_y

test_F1 = np.zeros(kfold)
time_k = np.zeros(kfold)
skf = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=random_state)
k = 0
epochs = 300
batch_size = 15

# class_weight = {0 : 1., 1: 1.,}  # The weights can be changed and made inversely proportional to the class size to improve the accuracy.
class_weight = {0 : 0.12, 1: 0.88,}

for train_index, test_index in skf.split(X, y):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    model = Sequential()
    model.add(Dense(128, input_shape=(X_train.shape[1],))) 
    model.add(Activation('relu'))
    model.add(Dropout(0.5))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.summary()
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    start_time = time.time()
    model.fit(X_train, y_train ,batch_size=batch_size, epochs=epochs, verbose=1, class_weight=class_weight)
    end_time = time.time()
    time_k[k] = end_time-start_time

    y_pred = model.predict_proba(X_test).round().astype(int)
    y_train_pred = model.predict_proba(X_train).round().astype(int)
    test_F1[k] = sklearn.metrics.f1_score(y_test, y_pred)
    k += 1
```

    Model: "sequential_10"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    dense_30 (Dense)             (None, 128)               4608      
    _________________________________________________________________
    activation_30 (Activation)   (None, 128)               0         
    _________________________________________________________________
    dropout_20 (Dropout)         (None, 128)               0         
    _________________________________________________________________
    dense_31 (Dense)             (None, 1)                 129       
    _________________________________________________________________
    activation_31 (Activation)   (None, 1)                 0         
    =================================================================
    Total params: 4,737
    Trainable params: 4,737
    Non-trainable params: 0
    _________________________________________________________________
    WARNING:tensorflow:sample_weight modes were coerced from
      ...
        to  
      ['...']
    Train on 74 samples
    Epoch 1/300
    74/74 [==============================] - 0s 7ms/sample - loss: 0.1487 - accuracy: 0.5270
    Epoch 2/300
    74/74 [==============================] - 0s 120us/sample - loss: 0.1421 - accuracy: 0.5000
    ...
    74/74 [==============================] - 0s 118us/sample - loss: 0.0299 - accuracy: 0.8784
    Epoch 300/300
    74/74 [==============================] - 0s 133us/sample - loss: 0.0296 - accuracy: 0.8649



```python
print ('Average f1 score', np.mean(test_F1))
print ('Average Run time', np.mean(time_k))
```

    Average f1 score 0.6341880341880342
    Average Run time 3.880180994669596


#### Building an LSTM Classifier on the sequences for comparison
We built an LSTM Classifier on the sequences to compare the accuracy.


```python
X = data['seq']
encoded_X = np.ndarray(shape=(len(X),), dtype=list)
for i in range(0,len(X)):
    encoded_X[i]=X.iloc[i].split("~")
X
```




    0      1~2~3~3~3~3~3~3~1~4~5~1~2~3~3~3~3~3~3~1~4~5~1~...
    1      6~5~5~6~5~6~5~2~5~5~5~5~5~5~5~5~5~5~5~5~5~5~5~...
    2      19~19~19~19~19~19~19~19~19~19~19~19~19~19~19~1...
    3      6~5~5~6~5~6~5~2~5~5~5~5~5~5~5~5~5~5~5~5~5~5~5~...
    4      5~5~17~5~5~5~5~5~10~2~11~2~11~11~12~11~11~5~2~...
                                 ...                        
    106    10~2~11~2~11~11~12~11~11~5~2~11~5~2~5~2~3~14~3...
    107    5~5~2~5~17~6~5~6~5~5~2~6~17~3~2~2~3~5~2~3~5~6~...
    108    6~5~6~5~5~6~5~5~6~6~6~6~6~6~6~6~6~6~6~6~6~6~6~...
    109    6~5~5~6~5~6~5~2~38~2~3~5~22~39~5~5~5~5~5~5~5~5...
    110    5~6~5~5~10~2~11~2~11~11~12~11~5~2~11~11~12~11~...
    Name: seq, Length: 111, dtype: object




```python
max_seq_length = np.max(data['seqlen'])
encoded_X = tf.keras.preprocessing.sequence.pad_sequences(encoded_X, maxlen=max_seq_length)
```


```python
kfold = 3
random_state = 11

test_F1 = np.zeros(kfold)
time_k = np.zeros(kfold)

epochs = 50
batch_size = 15
skf = StratifiedKFold(n_splits=kfold, shuffle=True, random_state=random_state)
k = 0

for train_index, test_index in skf.split(encoded_X, y):
    X_train, X_test = encoded_X[train_index], encoded_X[test_index]
    y_train, y_test = y[train_index], y[test_index]
    
    embedding_vecor_length = 32
    top_words=50
    model = Sequential()
    model.add(Embedding(top_words, embedding_vecor_length, input_length=max_seq_length))
    model.add(LSTM(32))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    model.summary()
    
    start_time = time.time()
    model.fit(X_train, y_train, epochs=epochs, batch_size=batch_size, verbose=1)
    end_time=time.time()
    time_k[k]=end_time-start_time

    y_pred = model.predict_proba(X_test).round().astype(int)
    y_train_pred=model.predict_proba(X_train).round().astype(int)
    test_F1[k]=sklearn.metrics.f1_score(y_test, y_pred)
    k+=1
```

    Model: "sequential_13"
    _________________________________________________________________
    Layer (type)                 Output Shape              Param #   
    =================================================================
    embedding (Embedding)        (None, 1773, 32)          1600      
    _________________________________________________________________
    lstm (LSTM)                  (None, 32)                8320      
    _________________________________________________________________
    dense_36 (Dense)             (None, 1)                 33        
    _________________________________________________________________
    activation_36 (Activation)   (None, 1)                 0         
    =================================================================
    Total params: 9,953
    Trainable params: 9,953
    Non-trainable params: 0
    _________________________________________________________________
    Train on 74 samples
    Epoch 1/50
    74/74 [==============================] - 5s 72ms/sample - loss: 0.6894 - accuracy: 0.5676
    Epoch 2/50
    74/74 [==============================] - 4s 48ms/sample - loss: 0.6590 - accuracy: 0.8784
    ...
    Epoch 50/50
    74/74 [==============================] - 4s 51ms/sample - loss: 0.1596 - accuracy: 0.9324



```python
print ('Average f1 score', np.mean(test_F1))
print ('Average Run time', np.mean(time_k))
```

    Average f1 score 0.36111111111111116
    Average Run time 192.46954011917114


We find that the LSTM classifier gives a significantly lower F1 score. This may be improved by changing the model. However, we find that the SGT embedding could work with a small and unbalanced data without the need of a complicated classifier model.

LSTM models typically require more data for training and also has significantly more computation time. The LSTM model above took 425.6 secs while the MLP model took just 9.1 secs.

## <a name="sequence-search"></a> Sequence Search

Sequence data sets are generally large. For example, sequences of listening history in music streaming services, such as Pandora, for more than 70M users are huge. In protein data bases there could be even larger size. For instance, the Uniprot data repository has more than 177M sequences.

Searching for similar sequences in such large data bases is challenging. SGT embedding provides a simple solution. In the following it will be shown on a protein data set that SGT embedding can be used to compute similarity between a query sequence and the sequence corpus using a dot product. The sequences with the highest dot product are returned as the most similar sequence to the query.

### Protein Sequence Search

In the following, a sample of 10k protein sequences are used for illustration. The data is taken from https://www.uniprot.org .


```python
# Loading data
data = pd.read_csv('data/protein-uniprot-reviewed-Ano-10k.tab', sep='\t')

# Data preprocessing
corpus = data.loc[:,['Entry','Sequence']]
corpus.columns = ['id', 'sequence']
corpus['sequence'] = corpus['sequence'].map(list)
corpus.head(3)
```




<div>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>id</th>
      <th>sequence</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>I2WKR6</td>
      <td>[M, V, H, K, S, D, S, D, E, L, A, A, L, R, A, ...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>A0A2A6M8K9</td>
      <td>[M, Q, E, S, L, V, V, R, R, E, T, H, I, A, A, ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>A0A3G5KEC3</td>
      <td>[M, A, S, G, A, Y, S, K, Y, L, F, Q, I, I, G, ...</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Protein sequence alphabets
alphabets = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 
             'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
             'W', 'X', 'Y', 'U', 'O']  # List of amino acids

# Alphabets are known and inputted 
# as arguments for faster computation
sgt_ = SGT(alphabets=alphabets, 
           lengthsensitive=True, 
           kappa=1, 
           flatten=True, 
           mode='multiprocessing')

sgtembedding_df = sgt_.fit_transform(corpus)
sgtembedding_df = sgtembedding_df.set_index('id')
```

    INFO: Pandarallel will run on 7 workers.
    INFO: Pandarallel will use standard multiprocessing data transfer (pipe) to transfer data between the main process and workers.



```python
'''
Search proteins similar to a query protein.
The approach is to find the SGT embedding of the
query protein and find its similarity with the
embeddings of the protein database.
'''

query_protein = 'MSHVFPIVIDDNFLSPQDLVSAARSGCSLRLHTGVVDKIDRAHRFVLEIAGAEALHYGINTGFGSLCTTHIDPADLSTLQHNLLKSHACGVGPTVSEEVSRVVTLIKLLTFRTGNSGVSLSTVNRIIDLWNHGVVGAIAQKGTVGASGDLAPLAHLFLPLIGLGQVWHRGVLRPSREVMDELKLAPLTLQPKDGLCLTNGVQYLNAWGALSTVRAKRLVALADLCAAMSMMGFSAARSFIEAQIHQTSLHPERGHVALHLRTLTHGSNHADLPHCNPAMEDPYSFRCAPQVHGAARQVVGYLETVIGNECNSVSDNPLVFPDTRQILTCGNLHGQSTAFALDFAAIGITDLSNISERRTYQLLSGQNGLPGFLVAKPGLNSGFMVVQYTSAALLNENKVLSNPASVDTIPTCHLQEDHVSMGGTSAYKLQTILDNCETILAIELMTACQAIDMNPGLQLSERGRAIYEAVREEIPFVKEDHLMAGLISKSRDLCQHSTVIAQQLAEMQAQ'

# Step 1. Compute sgt embedding for the query protein.
query_protein_sgt_embedding = sgt_.fit(list(query_protein))

# Step 2. Compute the dot product of query embedding 
# with the protein embedding database.
similarity = sgtembedding_df.dot(query_protein_sgt_embedding)

# Step 3. Return the top k protein names based on similarity.
similarity.sort_values(ascending=False)
```




    id
    K0ZGN5        2773.749663
    A0A0Y1CPH7    1617.451379
    A0A5R8LCJ1    1566.833152
    A0A290WY40    1448.772820
    A0A073K6N6    1392.267250
                     ...     
    A0A1S7UBK4     160.074989
    A0A2S7T1R9     156.580584
    A0A0E0UQV6     155.834932
    A0A1Y5Y0S0     148.862049
    B0NRP3         117.656497
    Length: 10063, dtype: float64



## <a name="sgt-spark"></a> SGT - Spark for Distributed Computing

As mentioned in the previous section, sequence data sets can be large. SGT complexity is linear with the number of sequences in a data set. Still if the data size is large the computation becomes high. For example, for a set of 1M protein sequences the default SGT mode takes over 24 hours.

Using distributed computing with Spark the runtime can be significantly reduced. For instance, SGT-Spark on the same 1M protein data set took less than 29 minutes.

In the following, Spark implementation for SGT is shown. First, it is applied on a smaller 10k data set for comparison. Then it is applied on 1M data set without any syntactical change.


```python
'''
Load the data and remove header.
'''
data = sc.textFile('data/protein-uniprot-reviewed-Ano-10k.tab')
 
header = data.first() #extract header
data = data.filter(lambda row: row != header)   #filter out header
data.take(1)  # See one sample

```

<div class="ansiout"><span class="ansired">Out[</span><span class="ansired">3</span><span class="ansired">]: </span>[&apos;I2WKR6\tI2WKR6_ECOLX\tunreviewed\tType III restriction enzyme, res subunit (EC 3.1.21.5)\tEC90111_4246\tEscherichia coli 9.0111\t786\tMVHKSDSDELAALRAENVRLVSLLEAHGIEWRRKPQSPVPRVSVLSTNEKVALFRRLFRGRDDVWALRWESKTSGKSGYSPACANEWQLGICGKPRIKCGDCAHRQLIPVSDLVIYHHLAGTHTAGMYPLLEDDSCYFLAVDFDEAEWQKDASAFMRSCDELGVPAALEISRSRQGAHVWIFFASRVSAREARRLGTAIISYTCSRTRQLRLGSYDRLFPNQDTMPKGGFGNLIALPLQKRPRELGGSVFVDMNLQPYPDQWAFLVSVIPMNVQDIEPTILRATGSIHPLDVNFINEEDLGTPWEEKKSSGNRLNIAVTEPLIITLANQIYFEKAQLPQALVNRLIRLAAFPNPEFYKAQAMRMSVWNKPRVIGCAENYPQHIALPRGCLDSALSFLRYNNIAAELIDKRFAGTECNAVFTGNLRAEQEEAVSALLRYDTGVLCAPTAFGKTVTAAAVIARRKVNTLILVHRTELLKQWQERLAVFLQVGDSIGIIGGGKHKPCGNIDIAVVQSISRHGEVEPLVRNYGQIIVDECHHIGAVSFSAILKETNARYLLGLTATPIRRDGLHPIIFMYCGAIRHTAARPKESLHNLEVLTRSRFTSGHLPSDARIQDIFREIALDHDRTVAIAEEAMKAFGQGRKVLVLTERTDHLDDIASVMNTLKLSPFVLHSRLSKKKRTMLISGLNALPPDSPRILLSTGRLIGEGFDHPPLDTLILAMPVSWKGTLQQYAGRLHREHTGKSDVRIIDFVDTAYPVLLRMWDKRQRGYKAMGYRIVADGEGLSF&apos;]</div>



```python
# Repartition for increasing the parallel processes
data = data.repartition(500)
```


```python
def preprocessing(line):
    '''
    Original data are lines where each line has \t
    separated values. We are interested in preserving
    the first value (entry id), tmp[0], and the last value
    (the sequence), tmp[-1].
    '''
    tmp = line.split('\t')
    id = tmp[0]
    sequence = list(tmp[-1])
    return (id, sequence)

processeddata = data.map(lambda line: preprocessing(line))
processeddata.take(1)  # See one sample

```


<div class="ansiout"><span class="ansired">Out[</span><span class="ansired">5</span><span class="ansired">]: </span>[(&apos;A0A2E9WIJ1&apos;,
  [&apos;M&apos;,
   &apos;Y&apos;,
   &apos;I&apos;,
   &apos;F&apos;,
   &apos;L&apos;,
   &apos;T&apos;,
   &apos;L&apos;,
	...   
   &apos;A&apos;,
   &apos;K&apos;,
   &apos;L&apos;,
   &apos;D&apos;,
   &apos;K&apos;,
   &apos;N&apos;,
   &apos;D&apos;])]</div>





```python
# Protein sequence alphabets
alphabets = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 
             'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
             'W', 'X', 'Y', 'U', 'O']  # List of amino acids
```


```python
'''
Spark approach.
In this approach the alphabets argument has to
be passed to the SGT class definition.
The SGT.fit() is then called in parallel.
'''
sgt_ = sgt.SGT(alphabets=alphabets, 
               kappa=1, 
               lengthsensitive=True, 
               flatten=True)
rdd = processeddata.map(lambda x: (x[0], list(sgt_.fit(x[1]))))
sgtembeddings = rdd.collect()
# Command took 29.66 seconds -- by cranjan@processminer.com at 4/22/2020, 12:31:23 PM on databricks
```

### Compare with the default SGT mode


```python
# Loading data
data = pd.read_csv('data/protein-uniprot-reviewed-Ano-10k.tab', sep='\t')

# Data preprocessing
corpus = data.loc[:,['Entry','Sequence']]
corpus.columns = ['id', 'sequence']
corpus['sequence'] = corpus['sequence'].map(list)

```


```python
sgt_ = sgt.SGT(alphabets=alphabets, 
               lengthsensitive=True, 
               kappa=1, 
               flatten=True, 
               mode='default')

sgtembedding_df = sgt_.fit_transform(corpus)
# Command took 13.08 minutes -- by cranjan@processminer.com at 4/22/2020, 1:48:02 PM on databricks
```

### 1M Protein Database

Protein 1M sequence data set is embedded here. The data set is available [here](https://mega.nz/file/1qAXhSAS#l7E60cLJzMGtFQzeHZL9PI8yX4tRQcAMFRN2xeHK81w).

```python
'''
Load the data and remove header.
'''
data = sc.textFile('data/protein-uniprot-reviewed-Ano-1M.tab')
 
header = data.first() #extract header
data = data.filter(lambda row: row != header)   #filter out header
data.take(1)  # See one sample
```



```python
# Repartition for increasing the parallel processes
data = data.repartition(10000)
```


```python
processeddata = data.map(lambda line: preprocessing(line))
processeddata.take(1)  # See one sample

# [('A0A2E9WIJ1',
#   ['M','Y','I','F','L','T','L','A','L','F','S',...,'F','S','I','F','A','K','L','D','K','N','D'])]
```


```python
# Protein sequence alphabets
alphabets = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 
             'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 
             'W', 'X', 'Y', 'U', 'O']  # List of amino acids
```


```python
'''
Spark approach.
In this approach the alphabets argument has to
be passed to the SGT class definition.
The SGT.fit() is then called in parallel.
'''
sgt_ = sgt.SGT(alphabets=alphabets, 
               kappa=1, 
               lengthsensitive=True, 
               flatten=True)
rdd = processeddata.map(lambda x: (x[0], list(sgt_.fit(x[1]))))
sgtembeddings = rdd.collect()
# Command took 28.98 minutes -- by cranjan@processminer.com at 4/22/2020, 3:16:41 PM on databricks
```


```python
'''OPTIONAL.
Save the embeddings for future use or 
production deployment.'''
# Save for deployment
# pickle.dump(sgtembeddings, 
#             open("data/protein-sgt-embeddings-1M.pkl", "wb"))
# The pickle dump is shared at https://mega.nz/file/hiAxAAoI#SStAIn_FZjAHvXSpXfdy8VpISG6rusHRf9HlUSqwcsw
# sgtembeddings = pickle.load(open("data/protein-sgt-embeddings-1M.pkl", "rb"))
```

The pickle dump is shared [here](https://mega.nz/file/hiAxAAoI#SStAIn_FZjAHvXSpXfdy8VpISG6rusHRf9HlUSqwcsw).

### Sequence Search using SGT - Spark

Since `sgtembeddings` on the 1M data set is large it is recommended to use distributed computing to find similar proteins during a search.


```python
sgtembeddings_rdd = sc.parallelize(list(dict(sgtembeddings).items()))
sgtembeddings_rdd = sgtembeddings_rdd.repartition(10000)
```


```python
'''
Search proteins similar to a query protein.
The approach is to find the SGT embedding of the
query protein and find its similarity with the
embeddings of the protein database.
'''

query_protein = 'MSHVFPIVIDDNFLSPQDLVSAARSGCSLRLHTGVVDKIDRAHRFVLEIAGAEALHYGINTGFGSLCTTHIDPADLSTLQHNLLKSHACGVGPTVSEEVSRVVTLIKLLTFRTGNSGVSLSTVNRIIDLWNHGVVGAIAQKGTVGASGDLAPLAHLFLPLIGLGQVWHRGVLRPSREVMDELKLAPLTLQPKDGLCLTNGVQYLNAWGALSTVRAKRLVALADLCAAMSMMGFSAARSFIEAQIHQTSLHPERGHVALHLRTLTHGSNHADLPHCNPAMEDPYSFRCAPQVHGAARQVVGYLETVIGNECNSVSDNPLVFPDTRQILTCGNLHGQSTAFALDFAAIGITDLSNISERRTYQLLSGQNGLPGFLVAKPGLNSGFMVVQYTSAALLNENKVLSNPASVDTIPTCHLQEDHVSMGGTSAYKLQTILDNCETILAIELMTACQAIDMNPGLQLSERGRAIYEAVREEIPFVKEDHLMAGLISKSRDLCQHSTVIAQQLAEMQAQ'

# Step 1. Compute sgt embedding for the query protein.
query_protein_sgt_embedding = sgt_.fit(list(query_protein))

# Step 2. Broadcast the embedding to the cluster.
query_protein_sgt_embedding_broadcasted = sc.broadcast(list(query_protein_sgt_embedding))

# Step 3. Compute similarity between each sequence embedding and the query.
similarity = sgtembeddings_rdd.map(lambda x: (x[0], 
                                              np.dot(query_protein_sgt_embedding_broadcasted.value, 
                                                     x[1]))).collect()

# Step 4. Show the most similar sequences with the query.
pd.DataFrame(similarity).sort_values(by=1, ascending=False)
```
