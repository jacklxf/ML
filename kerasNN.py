import numpy as np
import pandas as pd
from random import randint
import matplotlib.pyplot as plt

x=np.random.randint(13,100,size=1000).reshape(200,5)
y=np.random.randint(2,size=200)
print(x,y)




#pre-processing

from sklearn.preprocessing import MinMaxScaler
MMS=MinMaxScaler(feature_range=(0,1))
x_scaled=MMS.fit_transform(x)
print(x_scaled)
from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x_scaled,y,test_size=0.4,random_state=2)

import keras
from keras.models import Sequential
from keras import backend as K
from keras.layers.core import Dense
from keras.layers import Activation
from keras.optimizers import SGD,Adam

model=Sequential([Dense(10,input_shape=(5,),activation='tanh'),
                  Dense(8,activation='tanh'),
                  Dense(6,activation='tanh'),
                  Dense(3,activation='softmax')])
#print(model.summary())

model.compile(Adam(lr=.004), loss='sparse_categorical_crossentropy',metrics=['accuracy'])
model.fit(x_train,y_train,batch_size=10,epochs=20)
y_pred=model.predict(x_train)
'''
y_test_class=np.argmax(y_test)
print(y_test_class)
y_pred_class=np.argmax(y_pred)
print(y_pred_class)
'''
#Accuracy of the prediction
from sklearn import metrics
print(metrics.accuracy_score(y_test,y_pred))

