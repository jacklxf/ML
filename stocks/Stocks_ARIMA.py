import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.arima_model import ARIMA
import seaborn; seaborn.set()
from Stock_extract import extraction

df=extraction()

model=ARIMA(df['aapl'],order=(5,1,0))
model_fit=model.fit(disp=0)
print(model_fit.summary())
residuals=pd.DataFrame(model_fit.resid)
plt.plot(residuals)
plt.show()
residuals.plot(kind='kde')
plt.show()
print(residuals.describe())