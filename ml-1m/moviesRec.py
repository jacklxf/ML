imimport tensorflow as tf
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

#import data
rating=pd.read_csv('ratings.dat',sep='\s+',names=['user','item','rating','timestamp'])
rating=rating.drop('timestamp',axis=1)
print(rating.head())
num_items=rating.item.nunique()
num_users=rating.user.nunique()
print('items:',num_items,'users:',num_users)

#ratings normalization
print('Max rating:',max(rating.rating),'Min rating:',min(rating.rating))
MNS=MinMaxScaler()
rating_scaler=MNS.fit_transform(rating.rating.values.reshape(-1,1))
print(rating_scaler[:10])

#create weights and biases
def add_layer(y_true,in_size,out_size,activation_function=None):
    weights=tf.Variable(tf.random_normal([in_size,out_size]))
    biases=tf.Variable(tf.zeros([1,out_size])+0.1)
    y_pred=tf.add(tf.matmul(y_true,weights),biases)
    if activation_function is None:
        return y_pred
    else:
        y_pred=activation_function(y_pred)
        return y_pred

#setting loss, optimizer
y_pred=add_layer()
loss=tf.reduce_mean(tf.square(y_true-y_pred))
optimizer=tf.train.GradientDescentOptimizer(0.5)
train=optimizer.minimize(loss)
init=tf.initialize_all_variables()

#training model
with tf.Session() as sess:
    sess.run(init)
    for step in range(20):
        sess.run(train)
        if step %20==0:
            print(step,sess.run(weights),sess.run(biases))








