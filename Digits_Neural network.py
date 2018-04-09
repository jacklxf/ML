# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 15:02:47 2018

@author: xiaofeng.li
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.datasets import load_digits
from sklearn.cross_validation import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from sklearn import metrics

digits=load_digits()
X=digits.data
y=digits.target



X_train,X_test,y_train,y_test=train_test_split(X,y,test_size=0.4,random_state=3)

ss=StandardScaler()
X_train=ss.fit_transform(X_train)
mlp=MLPClassifier(hidden_layer_sizes=[500,400],alpha=0.1,activation='logistic')
mlp.fit(X_train,y_train)
y_pred=mlp.predict(X_test)

acc=metrics.accuracy_score(y_true=y_test,y_pred=y_pred)
print(acc)


