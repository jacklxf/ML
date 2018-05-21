from DataPreperation import *
import numpy as np
import pandas as pd
import tensorflow as tf
import matplotlib.pyplot as plt


num_items=rating['subgameID'].nunique()
num_users=rating['userID'].nunique()

x=tf.placeholder(tf.float32,[None,num_items])

weights1=tf.Variable(tf.random_normal([num_items,20],dtype=tf.float32))
biases1=tf.Variable(tf.random_normal([20],dtype=tf.float32))

weights2=tf.Variable(tf.random_normal([20,10],dtype=tf.float32))
biases2=tf.Variable(tf.random_normal([10],dtype=tf.float32))

weights3=tf.Variable(tf.random_normal([10,20],dtype=tf.float32))
biases3=tf.Variable(tf.random_normal([20],dtype=tf.float32))

weights4=tf.Variable(tf.random_normal([20,10],dtype=tf.float32))
biases4=tf.Variable(tf.random_normal([10],dtype=tf.float32))

weights5=tf.Variable(tf.random_normal([10,num_items],dtype=tf.float32))
biases5=tf.Variable(tf.random_normal([num_items],dtype=tf.float32))

def Layer(X):
    one_layer=tf.nn.sigmoid(tf.add(tf.matmul(X,weights1),biases1))
    two_layer=tf.nn.sigmoid(tf.add(tf.matmul(one_layer,weights2),biases2))
    three_layer=tf.nn.sigmoid(tf.add(tf.matmul(two_layer,weights3),biases3))
    four_layer=tf.nn.sigmoid(tf.add(tf.matmul(three_layer,weights4),biases4))
    five_layer=tf.nn.sigmoid(tf.add(tf.matmul(four_layer,weights5),biases5))
    return five_layer


y_pred=Layer(x)
y_true=x

loss=tf.losses.mean_squared_error(y_true,y_pred)
optimizer=tf.train.RMSPropOptimizer(learning_rate=0.04).minimize(loss)
init=tf.global_variables_initializer()
local_init=tf.local_variables_initializer()
predictions=pd.DataFrame()
matrix=rating_matrix.as_matrix()
users=rating_matrix.index.tolist()
items=rating_matrix.columns.tolist()

with tf.Session() as sess:
    sess.run(init)
    sess.run(local_init)
    num_batch=int(matrix.shape[0]/200)
    matrix_split=np.array_split(matrix,num_batch)
    step=[]
    cost=[]
    for i in range(500):
        sum_cost=0
        for batch_size in matrix_split:
            _,c=sess.run([optimizer,loss],feed_dict={x:batch_size})
            sum_cost=sum_cost+c
        mean_cost=sum_cost/num_batch
        print("Epoch:{} Loss:{}".format(i+1,mean_cost))
        step.append(i+1)
        cost.append(mean_cost)
    preds = sess.run(y_pred, feed_dict={x: matrix})
    recommendation=pd.DataFrame(preds,index=users,columns=items)
    print(recommendation.head())

plt.plot(step,cost)
plt.xlabel('step')
plt.ylabel('Loss')
plt.title('Neural Network for Recommendation')
plt.show()






