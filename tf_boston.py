from sklearn.datasets import load_boston
from sklearn.model_selection import train_test_split
import tensorflow as tf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

df=load_boston()
km=KMeans(n_clusters=3,random_state=0).fit(df.data)
print(km.labels_)
print(km.cluster_centers_)


