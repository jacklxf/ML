import numpy as np
import tensorflow as tf
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
df=load_iris()
#print(df)
X=df.data
Y=df.target
x_train,x_test,y_train,y_test=train_test_split(X,Y,test_size=0.2,random_state=1)

feature_columns=[tf.contrib.layers.real_valued_column("",dimension=4)]
classifier=tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                          hidden_units=[10,20,10],
                                          n_classes=3)
classifier.fit(x=x_train,y=y_train,steps=300)
accuracy_score=classifier.evaluate(x=x_test,y=y_test)["accuracy"]
print('Accuracy:{0:f}'.format(accuracy_score))
