import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import LSTM
import math

RawData=pd.read_csv('C:/Users/xiaofeng.li/Documents/ML/TimeSeriesDL/international-airline-passengers.csv',usecols=[1],engine='python',skipfooter=3)
dataset=RawData.values
dataset=dataset.astype('float32')
#print(dataset[:5])
#plt.plot(dataset)
#plt.show()

from sklearn.preprocessing import MinMaxScaler
scaler=MinMaxScaler()
dataset=scaler.fit_transform(dataset)

dataX,dataY=[],[]
for i in range(len(dataset)-1-1):
    dataX.append(dataset[i:(i+1),0])
    dataY.append(dataset[i+1,0])
dataX=np.array(dataX)
dataY=np.array(dataY)
print(dataX[:10])
print(dataY[:10])

train_size = int(len(dataset) * 0.67)
test_size = len(dataset) - train_size
train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

trainX,trainY=[],[]
for i in range(len(train)-1-1):
    trainX.append(train[i:(i+1),0])
    trainY.append(train[i+1,0])
trainX=np.array(trainX)
trainY=np.array(trainY)


testX,testY=[],[]
for i in range(len(test)-1-1):
    testX.append(test[i:(i+1),0])
    testY.append(test[i+1,0])
testX=np.array(testX)
testY=np.array(testY)

trainX=np.reshape(trainX, (trainX.shape[0], 1, trainX.shape[1]))
testX=np.reshape(testX, (testX.shape[0], 1, testX.shape[1]))


model=Sequential()
model.add(LSTM(8,input_shape=(1,1)))
model.add(Dense(1))
model.compile(loss='mean_squared_error',optimizer='adam')
model.fit(trainX,trainY,epochs=50,batch_size=1,verbose=2)

trainPredict=model.predict(trainX)
testPredict=model.predict(testX)

trainPredict=scaler.inverse_transform(trainPredict)
trainY=scaler.inverse_transform([trainY])
testPredict=scaler.inverse_transform(testPredict)
testY=scaler.inverse_transform([testY])

from sklearn.metrics import mean_squared_error
tranScore=math.sqrt(mean_squared_error(trainY[0],trainPredict[:,0]))
print('Train Score: %.2f RMSE' %(tranScore))
testScore=math.sqrt(mean_squared_error(testY[0],testPredict[:,0]))
print('test Score: %.2f RMSE' %(testScore))


# shift train predictions for plotting
trainPredictPlot = np.empty_like(dataset)
trainPredictPlot[:, :] = np.nan
trainPredictPlot[1:len(trainPredict)+1, :] = trainPredict

# shift test predictions for plotting
testPredictPlot = np.empty_like(dataset)
testPredictPlot[:, :] = np.nan
testPredictPlot[len(trainPredict)+(1*2)+1:len(dataset)-1, :] = testPredict

# plot baseline and predictions
plt.plot(scaler.inverse_transform(dataset))
plt.plot(trainPredictPlot)
plt.plot(testPredictPlot)
plt.show()