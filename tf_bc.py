import numpy as np
import pandas as pd
from sklearn import datasets
import tensorflow as tf
from sklearn.model_selection import train_test_split


df=datasets.load_breast_cancer()
print(df.data.shape) #(569, 30)
x_train,x_test,y_train,y_test=train_test_split(df.data,df.target,test_size=0.2,random_state=0)
print(x_train.shape,y_train.shape)
#(455, 30) (455,)


def dnnclass(x_train,x_test,y_train,y_test):
    feature_columns=[tf.contrib.layers.real_valued_column("",dimension=30)]
    classifier=tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                              hidden_units=[40,50,40],
                                              n_classes=2)

    classifier.fit(x=x_train,y=y_train,steps=3000)
    accuracy_score=classifier.evaluate(x=x_test,y=y_test)["accuracy"]
    print("Accuracy{0:f}".format(accuracy_score))

