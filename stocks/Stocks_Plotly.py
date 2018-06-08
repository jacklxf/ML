import plotly.plotly as py
from Stock_extract import *
import plotly.figure_factory as ff
import pandas as pd


#py.tools.set_credentials_file(username='xiaofeng.li',api_key='dNoeoZqvBKkPvtLBVPHj')

df=extraction()

table=ff.create_table(df)
py.plot(table,filename='Stocks trend')

