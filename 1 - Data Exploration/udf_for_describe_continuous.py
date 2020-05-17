# Import library
import pandas as pd
import numpy as np 
import seaborn as sns 
import matplotlib.pyplot as plt 
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.stats import kurtosis
from scipy.stats import skew
from scipy.stats import shapiro

# Definded function
## Class of formart text
class formart_text:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'


# Functinon for print table
def print_table(table, index_name= None):
    table= pd.DataFrame(table)
    for column in table.columns[table.dtypes != 'object']:
        table[column]= table[column].apply(lambda x: round(x, 2))
    if index_name != None:
        table= table.reset_index().rename(columns={'index': index_name})
    width= 500
    height= 130 + (table.shape[0] - 5) * 20
    if height > 300:
        height= 300
    layout = go.Layout(
                autosize=False,
                width= width, height= height,
                margin=go.layout.Margin(
                    l=30,
                    r=30,
                    b=0,
                    t=0,
                    pad = 4)
                )
    fig = go.Figure(data=[go.Table(
    header=dict(values=list(table.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values= [table[colum] for colum in table.columns],
               fill_color='lavender',
               align='left'))],
    layout= layout)
    
    fig.show()

# Functinon for create box plot
def create_hbox_plot(data, con_var):
    fig = go.Figure()
    fig.add_trace(go.Box(x= data[con_var], 
                         name= con_var,
                        boxpoints='outliers',
                        
                        marker=dict(
                                    color='rgb(8,81,156)',
                                    outliercolor='rgba(219, 64, 82, 0.6)',
                                    line=dict(
                                        outliercolor='rgba(219, 64, 82, 0.6)',
                                        outlierwidth=2)),
                                    line_color='rgb(8,81,156)',
                                    boxmean=True))
    fig.update_layout(
    autosize=False,
    width= 600, height= 200,
    margin=dict(
        l=0,
        r=0,
        b=0,
        t=0,
    ))
    
    fig.update_traces(boxpoints='all', jitter=0)
    
    fig.show()

# Functinon for create_histogram
def create_histogram(data, con_var):
    fig = px.histogram(data, x= con_var)
    fig.update_layout(
                    autosize=False,
                    width= 600, height= 400,
                    margin=dict(
                        l=0,
                        r=0,
                        b=0,
                        t=0,
                    ))
    fig.show()

def kurtosis_value(data, con_var):
    print("- Kurtosis : ",kurtosis(data[con_var]))

def skew_value(data, con_var):
    print("- Skew : ",skew(data[con_var]))

def shapiro_wilk_test(data, con_var):
    stat, p = shapiro(data[con_var])
    print('- Shapiro-Wilk test: Statistics= %.3f, p= %.3f' % (stat, p))

def describe_continuous_variable(data, con_var):
    n_string= int((80 - len(con_var)) / 2)
    print(formart_text.GREEN + '-' * n_string + con_var +'-' * n_string + formart_text.END)

    # con_var= 'LotArea'
    data[con_var]= pd.to_numeric(data[con_var]) # Convert variable to continuous

    ## Print Describe of variable
    n_record= data.shape[0] # Number of records in dataset
    n_na= data[con_var].isna().sum() # Number of missing values
    per_na= (n_na * 100)/ n_record # Percentage of missing values
    if int(per_na) == per_na:
        per_na= int(per_na)
    else:
        per_na= round(per_na, 2)
    n_available= data[con_var].count() # Number of available values
    per_available= (n_available * 100)/ n_record # Percentage of available values
    if int(per_available) == per_available:
        per_available= int(per_available)
    else:
        per_available= round(per_available, 2)

    print('* Describe:'.upper())
    print('- Number of records in dataset:', n_record)    
    print('- Number of missing values in {con_var} variable: {n_na} ({per_na}%)'
           .format(con_var= con_var, n_na= n_na, per_na= per_na))
    print('- Number of available values in {con_var} variable: {n_available} ({per_available}%)'
           .format(con_var= con_var, n_available= n_available, per_available= per_available))

    describe_table= data[con_var].describe()
    print_table(describe_table, index_name= '')

    print('* Box plot:'.upper())
    create_hbox_plot(data= data,con_var= con_var)
    print('* Histogram:'.upper())
    create_histogram(data= data,con_var= con_var)

    print('* Test for normality:'.upper())
    kurtosis_value(data= data,con_var= con_var)
    skew_value(data= data,con_var= con_var)
    shapiro_wilk_test(data= data,con_var= con_var)

