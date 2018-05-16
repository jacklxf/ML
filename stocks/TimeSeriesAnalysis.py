from StockAnalysis import extraction
import matplotlib.pyplot as plt

df=extraction()
for i in df.columns:

    plt.plot(df[i])
    plt.xlabel('Time')
    plt.legend()
    plt.show()



