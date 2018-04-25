import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import matplotlib.pyplot as plt

# import data
dataset = pd.read_csv('ratings.dat', sep='\s+', names=['user', 'item', 'rating', 'timestamp'])
dataset = dataset.drop('timestamp', axis=1)
num_items = dataset.item.nunique()
num_users = dataset.user.nunique()
print(num_items, num_users)

dataset.user = dataset.user.astype('category').cat.codes.values
dataset.item = dataset.item.astype('category').cat.codes.values

from sklearn.model_selection import train_test_split

train, test = train_test_split(dataset, test_size=0.2)

import keras
from IPython.display import SVG
from keras.optimizers import Adam
from keras.utils.vis_utils import model_to_dot

n_users, n_movies = len(dataset.user.unique()), len(dataset.item.unique())
n_latent_factors = 3

movie_input = keras.layers.Input(shape=[1], name='Item')
movie_embedding = keras.layers.Embedding(n_movies + 1, n_latent_factors, name='Movie-Embedding')(movie_input)
movie_vec = keras.layers.Flatten(name='FlattenMovies')(movie_embedding)

user_input = keras.layers.Input(shape=[1], name='User')
user_vec = keras.layers.Flatten(name='FlattenUsers')(
    keras.layers.Embedding(n_users + 1, n_latent_factors, name='User-Embedding')(user_input))

prod = keras.layers.merge([movie_vec, user_vec], mode='dot', name='DotProduct')
model = keras.Model([user_input, movie_input], prod)
model.compile('adam', 'mean_squared_error')

history = model.fit([train.user, train.item], train.rating, epochs=100, verbose=0)

pd.Series(history.history['loss']).plot(logy=True)
plt.xlabel("Epoch")
plt.ylabel("Train Error")

y_hat = np.round(model.predict([test.user, test.item]), 0)
y_true = test.rating

from sklearn.metrics import mean_absolute_error

mean_absolute_error(y_true, y_hat)

movie_embedding_learnt = model.get_layer(name='Movie-Embedding').get_weights()[0]
print(pd.DataFrame(movie_embedding_learnt).describe())

user_embedding_learnt = model.get_layer(name='User-Embedding').get_weights()[0]
print(pd.DataFrame(user_embedding_learnt).describe())
